# Implementation Plan: SQLite Routing Backend

## Overview

This plan implements the SQLite persistence backend for data_squirrel incrementally. We start with the foundational types and protocol, build the core SQLiteDataOperations class, modify existing classes to support backend switching, then add comprehensive tests. Each step builds on the previous and ends with wiring into the existing system.

## Tasks

- [x] 1. Create BackendType enum and DataOperationsProtocol
  - [x] 1.1 Create `src/data_squirrel/config/backend_types.py` with BackendType enum (YAML, SQLITE variants)
    - Define the enum with string values
    - _Requirements: 10.1_
  - [x] 1.2 Add DataOperationsProtocol class to `src/data_squirrel/config/backend_types.py`
    - Define Protocol with `save_data(data, working_folder, nut_name, filename)` and `read_data(working_folder, nut_name, filename)` method signatures
    - Import Protocol from typing
    - _Requirements: 10.7_

- [x] 2. Implement SQLiteDataOperations class
  - [x] 2.1 Create `src/data_squirrel/config/nut_sqlite_operations.py` with SQLiteDataOperations class skeleton
    - Implement `__init__` that validates working_folder exists, creates DB path, and calls `_init_db()`
    - Implement `_init_db()` that creates the `nut_values` table with columns: address_key (TEXT PRIMARY KEY), value_type (TEXT NOT NULL), value_data (TEXT NOT NULL), nut_name (TEXT NOT NULL)
    - Implement `_make_address_key()` helper that joins address list with `"|"` separator
    - Implement `_extract_address_from_filename()` helper that derives address_list from the filename Path parameter
    - Raise FileNotFoundError if working_folder does not exist
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 8.1_
  - [x] 2.2 Implement `save_data` for primitive types (String, Integer, FloatingPoint)
    - Serialize value as JSON `{"value": <val>}`
    - Use INSERT OR REPLACE to store with value_type STRING/INTEGER/FLOAT
    - Commit after each write
    - Raise ValueError for unsupported types with non-None values
    - _Requirements: 2.1, 2.2, 2.3, 2.6, 4.2, 4.3, 8.2, 8.3_
  - [x] 2.3 Implement `save_data` for Dictionary type
    - Serialize as JSON with key_def, value_def, and value fields
    - Map NutObjectType enum values to string type identifiers
    - _Requirements: 2.4, 4.4_
  - [x] 2.4 Implement `save_data` for ListOfThings type
    - Serialize as JSON with value_def and value fields
    - _Requirements: 2.5, 4.4_
  - [x] 2.5 Implement `save_data` for dataclass instances
    - Detect dataclass via `dataclasses.is_dataclass()`
    - Serialize fields individually with module/attribute metadata
    - Raise TypeError if dataclass type is not registered in external_imports
    - _Requirements: 9.1, 9.3, 9.4, 9.5, 9.6_
  - [x] 2.6 Implement `read_data` for all types
    - Parse address key from filename parameter
    - Query database by address_key
    - Raise KeyError if address not found
    - Deserialize based on value_type: reconstruct String, Integer, FloatingPoint, Dictionary, ListOfThings, or dataclass instances
    - For dataclass: import class from module/attribute path and reconstruct
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 9.2, 9.8_

- [x] 3. Modify NutFilterDefinitions to support backend switching
  - [x] 3.1 Update `NutFilterDefinitions.__init__` to accept `backend_type` parameter (default BackendType.SQLITE)
    - Import BackendType and SQLiteDataOperations
    - Instantiate SQLiteDataOperations when SQLITE, YamlDataOperations when YAML
    - Raise ValueError for unsupported backend types
    - Replace `self.yaml_operations` with `self.operations` (generic name)
    - _Requirements: 5.1, 10.3, 10.4, 10.6, 10.8_
  - [x] 3.2 Update `filter_out_flow` and `filter_in_flow` to use `self.operations` instead of the `ops` parameter
    - Change method signatures to use the instance's operations object
    - Maintain all existing type decomposition and routing logic unchanged
    - _Requirements: 5.2, 5.3, 5.4_

- [x] 4. Modify Nut class to accept BackendType parameter
  - [x] 4.1 Update `Nut` class in `dynamic_data_nut.py` to accept `backend_type` field (default BackendType.SQLITE)
    - Add `backend_type: BackendType` field with default
    - Pass backend_type to NutFilterDefinitions in `__attrs_post_init__`
    - _Requirements: 10.2, 10.5_

- [x] 5. Checkpoint - Core implementation verification
  - Ensure all core code compiles without errors, ask the user if questions arise.

- [x] 6. Unit tests for SQLiteDataOperations
  - [x] 6.1 Create `src/test/test_sqlite_operations.py` with test fixtures
    - Set up tmp_path-based working folders for isolated test databases
    - Create helper functions for instantiating SQLiteDataOperations
    - _Requirements: 11.1_
  - [x] 6.2 Write unit tests for database initialization
    - Test that DB file is created on instantiation
    - Test that nut_values table exists
    - Test FileNotFoundError for missing working folder
    - _Requirements: 11.1, 11.7_
  - [x] 6.3 Write unit tests for primitive save/read (String, Integer, FloatingPoint)
    - Test save and read for each primitive type
    - Verify type preservation (int stays int, not float)
    - _Requirements: 11.2, 11.3, 11.4_
  - [x] 6.4 Write unit tests for Dictionary and ListOfThings save/read
    - Test dict with various key/value type combinations
    - Test list with various item types
    - _Requirements: 11.5, 11.6_
  - [x] 6.5 Write unit tests for error conditions
    - Test read from non-existent address raises KeyError
    - Test unsupported type raises ValueError
    - _Requirements: 11.7, 11.8_

- [x] 7. Integration tests for full routing pipeline
  - [x] 7.1 Create `src/test/test_sqlite_routing.py` with integration test fixtures
    - Set up Nut instances with BackendType.SQLITE
    - Create enum-based attribute structures for testing
    - _Requirements: 11.15_
  - [x] 7.2 Write integration tests for outbound/inbound flow
    - Test full set-then-get pipeline for str, int, float, dict, list
    - Verify values pass through NutFilterDefinitions and are persisted correctly
    - Test multiple attributes stored at distinct addresses
    - _Requirements: 11.15, 11.16, 11.17, 11.18_
  - [x] 7.3 Create `src/test/test_backend_switching.py` for BackendType enum switching tests
    - Test that YAML and SQLITE backends produce equivalent results for primitives
    - Test that YAML and SQLITE backends produce equivalent results for complex types
    - _Requirements: 11.19, 11.20, 11.21, 11.22_

- [x] 8. Checkpoint - Tests passing
  - Ensure all tests pass, ask the user if questions arise.

- [x] 9. Edge case tests
  - [x] 9.1 Create `src/test/test_sqlite_edge_cases.py`
    - Test empty dictionary round-trip
    - Test empty list round-trip
    - Test None value handling (graceful, no crash)
    - Test overwrite at same address returns new value
    - Test read from never-written address raises descriptive error
    - Test unsupported type raises ValueError with descriptive message
    - _Requirements: 11.23, 11.24, 11.25, 11.26, 11.27, 11.28_

- [ ] 10. Property-based tests with Hypothesis
  - [ ]* 10.1 Create `src/test/test_sqlite_properties.py` with Hypothesis setup
    - Add hypothesis import and settings configuration (max_examples=200)
    - Create helper fixtures for temporary SQLiteDataOperations instances
    - _Requirements: 11.29_
  - [ ]* 10.2 Write property test for primitive value round-trip
    - **Property 1: Primitive value round-trip**
    - Strategy: `one_of(text(), integers(), floats(allow_nan=False, allow_infinity=False))`
    - Verify `type(result) == type(original)` and `result == original`
    - **Validates: Requirements 6.1, 6.4, 11.29, 11.30, 11.31**
  - [ ]* 10.3 Write property test for dictionary round-trip
    - **Property 2: Dictionary round-trip**
    - Strategy: `dictionaries(keys=one_of(text(), integers()), values=one_of(text(), integers(), floats(allow_nan=False)))`
    - **Validates: Requirements 6.2, 11.32**
  - [ ]* 10.4 Write property test for list round-trip
    - **Property 3: List round-trip**
    - Strategy: `lists(one_of(text(), integers(), floats(allow_nan=False, allow_infinity=False)))`
    - **Validates: Requirements 6.3, 11.33**
  - [ ]* 10.5 Write property test for dataclass round-trip
    - **Property 4: Dataclass round-trip**
    - Custom strategy generating dataclass instances with primitive fields
    - **Validates: Requirements 9.7, 11.34**
  - [ ]* 10.6 Write property test for overwrite semantics
    - **Property 5: Overwrite semantics (last write wins)**
    - Two values of same type + random address
    - **Validates: Requirements 4.3**
  - [ ]* 10.7 Write property test for address list acceptance
    - **Property 6: Address list acceptance**
    - Strategy: `lists(text(min_size=1, alphabet=characters(whitelist_categories=('L', 'N'))), min_size=1)`
    - **Validates: Requirements 4.1, 7.3**
  - [ ]* 10.8 Write property test for backend equivalence
    - **Property 7: Backend equivalence**
    - Strategy: `one_of(text(), integers(), floats(allow_nan=False, allow_infinity=False))`
    - Verify SQLite and YAML produce same results
    - **Validates: Requirements 10.7**

- [x] 11. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties from the design document
- Unit tests validate specific examples and edge cases
- The `hypothesis` library must be added as a test dependency in `pyproject.toml` or `setup.cfg`
