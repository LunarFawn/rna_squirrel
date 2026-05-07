# Requirements Document

## Introduction

This feature modifies the existing data routing and persistence layer in data_squirrel to use Python's built-in `sqlite3` module instead of the current YAML file-based storage. The current system routes attribute values through `NutFilterDefinitions` and `NutAdressing` classes, serializing data to individual YAML files via `YamlDataOperations`. This change replaces that YAML persistence backend with SQLite while preserving the existing routing, addressing, and type-handling semantics.

## Glossary

- **Router**: The `NutFilterDefinitions` class that intercepts attribute get/set operations and directs data to the persistence backend based on flow direction (INBOUND or OUTBOUND).
- **Addressing_System**: The `NutAdressing` class that builds hierarchical address paths by walking the parent attribute chain to determine where data should be stored.
- **Persistence_Backend**: The storage layer responsible for saving and retrieving typed values. Currently `YamlDataOperations` using YAML files; to be replaced with an SQLite-based implementation.
- **Value_Packet**: A `ValuePacket` object that wraps a value with its name, type, and parent reference for routing through the system.
- **Address_Info**: An `AddressInfo` object containing the resolved address list, working folder, and file path for a given attribute.
- **Nut**: The top-level dynamic data container that holds typed attributes organized in a hierarchical structure.
- **Custom_Attribute**: A `CustomAttribute` instance representing a node in the attribute hierarchy, intercepting get/set for routing.
- **SQLite_Backend**: The new persistence implementation using Python's built-in `sqlite3` module to store and retrieve typed attribute values.
- **Dataclass_Instance**: A Python object that is an instance of a class decorated with `@dataclass`, whose fields are stored and reconstructed individually during serialization.
- **External_Import**: An `ExternalAttribute` entry in `NutStructure.external_imports` that specifies the module path and class name needed to import and reconstruct a dataclass type during deserialization.
- **BackendType**: A Python `Enum` class with variants (at minimum `YAML` and `SQLITE`) that determines which persistence backend the system uses for data storage and retrieval.
- **Test_Suite**: The collection of pytest-based test modules in `src/test/` that verify the correctness of the SQLite routing interface through unit tests, integration tests, edge case tests, and property-based tests (using the Hypothesis library).

## Requirements

### Requirement 1: SQLite Database Initialization

**User Story:** As a developer, I want the system to create and initialize an SQLite database when a Nut is instantiated, so that data can be persisted without requiring external dependencies.

#### Acceptance Criteria

1. WHEN a Nut is instantiated with a working folder path, THE SQLite_Backend SHALL create an SQLite database file in the specified working folder if one does not already exist.
2. WHEN the SQLite database is created, THE SQLite_Backend SHALL create the necessary tables for storing typed attribute values.
3. IF the working folder path does not exist, THEN THE SQLite_Backend SHALL raise a FileNotFoundError with a descriptive message.
4. WHEN a Nut is instantiated with a working folder that already contains an SQLite database, THE SQLite_Backend SHALL open the existing database without data loss.

### Requirement 2: Outbound Data Routing to SQLite

**User Story:** As a developer, I want attribute values to be persisted to SQLite when set on a Custom_Attribute, so that data is stored durably without YAML file overhead.

#### Acceptance Criteria

1. WHEN a Value_Packet with a string type is routed outbound, THE SQLite_Backend SHALL store the value in the database keyed by its address path.
2. WHEN a Value_Packet with an integer type is routed outbound, THE SQLite_Backend SHALL store the value in the database keyed by its address path.
3. WHEN a Value_Packet with a float type is routed outbound, THE SQLite_Backend SHALL store the value in the database keyed by its address path.
4. WHEN a Value_Packet with a dict type is routed outbound, THE SQLite_Backend SHALL store the dictionary with its key type definition and value type definition in the database.
5. WHEN a Value_Packet with a list type is routed outbound, THE SQLite_Backend SHALL store the list with its item type definition in the database.
6. IF a Value_Packet contains an unsupported type and a non-None value, THEN THE SQLite_Backend SHALL raise a ValueError indicating the type is unsupported.

### Requirement 3: Inbound Data Routing from SQLite

**User Story:** As a developer, I want attribute values to be retrieved from SQLite when accessed on a Custom_Attribute, so that previously stored data is correctly reconstructed.

#### Acceptance Criteria

1. WHEN a string value is retrieved from the database, THE SQLite_Backend SHALL return the value as a Python str.
2. WHEN an integer value is retrieved from the database, THE SQLite_Backend SHALL return the value as a Python int.
3. WHEN a float value is retrieved from the database, THE SQLite_Backend SHALL return the value as a Python float.
4. WHEN a dictionary value is retrieved from the database, THE SQLite_Backend SHALL reconstruct the dictionary with correctly typed keys and values based on stored type definitions.
5. WHEN a list value is retrieved from the database, THE SQLite_Backend SHALL reconstruct the list with correctly typed items based on the stored type definition.
6. IF a requested address path does not exist in the database, THEN THE SQLite_Backend SHALL raise an appropriate error.

### Requirement 4: Address-Based Storage Schema

**User Story:** As a developer, I want data to be stored using the hierarchical address path as the key, so that the existing addressing and routing logic remains compatible.

#### Acceptance Criteria

1. THE SQLite_Backend SHALL use the address list produced by the Addressing_System as the unique key for each stored value.
2. WHEN a value is stored, THE SQLite_Backend SHALL record the value type alongside the value data so that correct deserialization is possible on retrieval.
3. WHEN a value is updated at an existing address, THE SQLite_Backend SHALL overwrite the previous value at that address.
4. THE SQLite_Backend SHALL store complex types (dict, list) in a serialized format that preserves type metadata for keys, values, and items.

### Requirement 5: Router Integration

**User Story:** As a developer, I want the Router to use the SQLite_Backend instead of YamlDataOperations, so that the persistence switch is transparent to the rest of the system.

#### Acceptance Criteria

1. WHEN NutFilterDefinitions is instantiated, THE Router SHALL initialize the SQLite_Backend with the provided working directory.
2. WHEN filter_out_flow is called with a Value_Packet, THE Router SHALL delegate persistence to the SQLite_Backend save operation.
3. WHEN filter_in_flow is called, THE Router SHALL delegate retrieval to the SQLite_Backend read operation.
4. THE Router SHALL preserve the existing ValueFlow enum semantics (OUTBOUND, INBOUND) without modification.

### Requirement 6: Type Fidelity Round-Trip

**User Story:** As a developer, I want values stored and retrieved through the SQLite backend to maintain their original Python types, so that data integrity is preserved.

#### Acceptance Criteria

1. FOR ALL supported primitive types (str, int, float), storing a value and then retrieving it at the same address SHALL produce a value equal to the original.
2. FOR ALL supported dict values with typed keys and values, storing and then retrieving SHALL produce a dictionary equal to the original.
3. FOR ALL supported list values with typed items, storing and then retrieving SHALL produce a list equal to the original.
4. THE SQLite_Backend SHALL preserve the distinction between int and float values (storing 1 as int SHALL NOT return 1.0 as float).

### Requirement 7: Backward Compatibility of Addressing

**User Story:** As a developer, I want the NutAdressing class to continue working without modification, so that existing attribute hierarchy traversal logic is unaffected.

#### Acceptance Criteria

1. THE Addressing_System SHALL continue to produce address lists by walking the parent attribute chain.
2. THE Addressing_System SHALL remain independent of the persistence backend implementation.
3. WHEN the Addressing_System produces an address list, THE SQLite_Backend SHALL accept that address list as a valid storage key without transformation.

### Requirement 8: Database Connection Management

**User Story:** As a developer, I want SQLite connections to be managed properly, so that data is not corrupted and resources are released appropriately.

#### Acceptance Criteria

1. THE SQLite_Backend SHALL use a single database file per Nut working folder.
2. WHEN multiple write operations occur in sequence, THE SQLite_Backend SHALL ensure each write is committed to the database.
3. IF a write operation fails, THEN THE SQLite_Backend SHALL raise an exception without leaving the database in a corrupted state.
4. THE SQLite_Backend SHALL handle concurrent read operations from the same process without error.

### Requirement 9: Dataclass Serialization and Deserialization

**User Story:** As a developer, I want to store and retrieve Python dataclass instances through the SQLite routing system, so that externally imported dataclass types are fully supported as attribute values.

#### Acceptance Criteria

1. WHEN a Value_Packet with a dataclass instance is routed outbound, THE SQLite_Backend SHALL serialize the dataclass by storing each of its fields as individual typed values keyed under the instance's address path.
2. WHEN a dataclass value is retrieved from the database, THE SQLite_Backend SHALL reconstruct the dataclass instance by reading the stored fields and passing them to the dataclass constructor.
3. WHEN a dict value contains dataclass instances as values, THE SQLite_Backend SHALL serialize each dataclass instance within the dictionary using the same field-level storage strategy.
4. WHEN a list value contains dataclass instances as items, THE SQLite_Backend SHALL serialize each dataclass instance within the list using the same field-level storage strategy.
5. THE SQLite_Backend SHALL require the dataclass type to be registered as an ExternalAttribute in the NutStructure external_imports list so that the correct class can be resolved during deserialization.
6. IF a dataclass instance is routed outbound but its type is not registered in external_imports, THEN THE SQLite_Backend SHALL raise a TypeError indicating the dataclass type is not importable.
7. FOR ALL registered dataclass types with fields of supported primitive types (str, int, float), storing a dataclass instance and then retrieving it at the same address SHALL produce an instance equal to the original (round-trip property).
8. WHEN a dataclass is reconstructed during inbound routing, THE SQLite_Backend SHALL import the class using the module and attribute paths defined in the corresponding ExternalAttribute entry.

### Requirement 10: Backend Selection via Enum

**User Story:** As a developer, I want to select the persistence backend at Nut initialization time using an enum, so that I can switch between YAML and SQLite storage without changing application logic.

#### Acceptance Criteria

1. THE BackendType enum SHALL define at least two variants: YAML and SQLITE.
2. WHEN a Nut is instantiated, THE Nut SHALL accept a BackendType parameter that specifies which persistence backend to use.
3. WHEN BackendType.SQLITE is provided, THE NutFilterDefinitions SHALL instantiate SQLiteDataOperations as the persistence backend.
4. WHEN BackendType.YAML is provided, THE NutFilterDefinitions SHALL instantiate YamlDataOperations as the persistence backend.
5. IF no BackendType parameter is provided at Nut initialization, THEN THE Nut SHALL default to BackendType.SQLITE.
6. THE NutFilterDefinitions SHALL propagate the BackendType value received from the Nut to determine which operations class to use.
7. THE SQLiteDataOperations and YamlDataOperations SHALL satisfy the same interface contract for save and read operations, ensuring either backend can be used interchangeably by the Router.
8. IF an unsupported BackendType variant is provided, THEN THE NutFilterDefinitions SHALL raise a ValueError indicating the backend type is not recognized.

### Requirement 11: Unit and Integration Tests for SQLite Interface

**User Story:** As a developer, I want comprehensive unit and integration tests for the SQLite routing interface, so that correctness, type fidelity, and backend interchangeability are verified automatically.

#### Acceptance Criteria

##### Unit Tests — SQLiteDataOperations

1. WHEN SQLiteDataOperations is instantiated with a valid working folder, THE Test_Suite SHALL verify that the SQLite database file is created and the required tables exist.
2. WHEN save_data is called with a String value, THE Test_Suite SHALL verify the value is persisted and can be read back unchanged.
3. WHEN save_data is called with an Integer value, THE Test_Suite SHALL verify the value is persisted and can be read back unchanged.
4. WHEN save_data is called with a FloatingPoint value, THE Test_Suite SHALL verify the value is persisted and can be read back unchanged.
5. WHEN save_data is called with a Dictionary value, THE Test_Suite SHALL verify the dictionary and its key/value type definitions are persisted and can be read back unchanged.
6. WHEN save_data is called with a ListOfThings value, THE Test_Suite SHALL verify the list and its item type definition are persisted and can be read back unchanged.
7. IF save_data is called with an address path that does not have an initialized folder, THEN THE Test_Suite SHALL verify that a FileNotFoundError or equivalent error is raised.
8. IF read_data is called for an address path that has no stored value, THEN THE Test_Suite SHALL verify that an appropriate error is raised.

##### Unit Tests — Type Serialization/Deserialization Round-Trips

9. FOR ALL str values, THE Test_Suite SHALL verify that serializing to the SQLite storage format and deserializing back produces a value equal to the original (round-trip property).
10. FOR ALL int values, THE Test_Suite SHALL verify that serializing and deserializing produces a value equal to the original, preserving int type (not float).
11. FOR ALL float values, THE Test_Suite SHALL verify that serializing and deserializing produces a value equal to the original, preserving float type (not int).
12. FOR ALL dict values with supported key types (str, int, float) and supported value types (str, int, float, list), THE Test_Suite SHALL verify that serializing and deserializing produces a dictionary equal to the original with correct key and value types.
13. FOR ALL list values with supported item types (str, int, float), THE Test_Suite SHALL verify that serializing and deserializing produces a list equal to the original with correct item types.
14. FOR ALL registered dataclass instances with fields of supported primitive types, THE Test_Suite SHALL verify that serializing and deserializing produces an instance equal to the original (round-trip property per Requirement 6 and Requirement 9).

##### Integration Tests — Full Routing Pipeline

15. WHEN a Custom_Attribute value is set (outbound flow), THE Test_Suite SHALL verify the value passes through NutFilterDefinitions, is routed via the Addressing_System, and is persisted by SQLiteDataOperations to the database.
16. WHEN a Custom_Attribute value is read (inbound flow), THE Test_Suite SHALL verify the value is retrieved from SQLiteDataOperations, passes through NutFilterDefinitions, and is returned with the correct type and value.
17. FOR ALL supported types (str, int, float, dict, list, dataclass), THE Test_Suite SHALL verify the full set-then-get pipeline produces a value equal to the original.
18. WHEN multiple attributes are set on the same Nut instance, THE Test_Suite SHALL verify each attribute is stored at a distinct address and can be retrieved independently.

##### Integration Tests — BackendType Enum Switching

19. WHEN a Nut is instantiated with BackendType.YAML and a value is stored and retrieved, THE Test_Suite SHALL record the result.
20. WHEN a Nut is instantiated with BackendType.SQLITE and the same value is stored and retrieved, THE Test_Suite SHALL verify the result is equivalent to the YAML backend result.
21. FOR ALL supported primitive types (str, int, float), THE Test_Suite SHALL verify that BackendType.YAML and BackendType.SQLITE produce equivalent round-trip results.
22. FOR ALL supported complex types (dict, list), THE Test_Suite SHALL verify that BackendType.YAML and BackendType.SQLITE produce equivalent round-trip results.

##### Edge Case Tests

23. WHEN an empty dictionary is stored and retrieved, THE Test_Suite SHALL verify the result is an empty dictionary without error.
24. WHEN an empty list is stored and retrieved, THE Test_Suite SHALL verify the result is an empty list without error.
25. WHEN a None value is provided in a Value_Packet, THE Test_Suite SHALL verify the system handles it gracefully without raising an unexpected exception.
26. IF a read is attempted for an address that was never written, THEN THE Test_Suite SHALL verify a descriptive error is raised.
27. IF an unsupported type is provided in a Value_Packet, THEN THE Test_Suite SHALL verify a ValueError is raised with a descriptive message.
28. WHEN a value is stored at an address and then a new value is stored at the same address, THE Test_Suite SHALL verify the second value overwrites the first and is returned on subsequent reads.

##### Property-Based Tests — Type Fidelity Round-Trip

29. FOR ALL randomly generated str values (including empty strings, unicode, and special characters), THE Test_Suite SHALL use property-based testing to verify the SQLite round-trip preserves the original value exactly.
30. FOR ALL randomly generated int values (including zero, negative, and large integers), THE Test_Suite SHALL use property-based testing to verify the SQLite round-trip preserves the original value and type exactly.
31. FOR ALL randomly generated float values (including zero, negative, and small floats), THE Test_Suite SHALL use property-based testing to verify the SQLite round-trip preserves the original value and type exactly.
32. FOR ALL randomly generated dict values with supported key/value type combinations, THE Test_Suite SHALL use property-based testing to verify the SQLite round-trip preserves the dictionary structure, types, and values exactly.
33. FOR ALL randomly generated list values with supported item types, THE Test_Suite SHALL use property-based testing to verify the SQLite round-trip preserves the list contents and item types exactly.
34. FOR ALL randomly generated dataclass instances with supported field types, THE Test_Suite SHALL use property-based testing to verify the SQLite round-trip produces an instance equal to the original.
