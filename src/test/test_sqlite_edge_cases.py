"""Edge case tests for SQLiteDataOperations.

Tests empty collections, None handling, overwrite semantics,
missing address errors, and unsupported type errors.
"""

import pytest
from pathlib import Path

from data_squirrel.config.nut_sqlite_operations import SQLiteDataOperations
from data_squirrel.config.nut_yaml_objects import (
    String,
    Integer,
    FloatingPoint,
    Dictionary,
    ListOfThings,
    NutObjectType,
)


# --- Helpers ---


def make_ops(tmp_path: Path) -> SQLiteDataOperations:
    """Create a SQLiteDataOperations instance with a temporary working folder."""
    return SQLiteDataOperations(working_folder=tmp_path)


def make_filename(working_folder: Path, address_list: list) -> Path:
    """Build a filename Path matching the expected format.

    Format: working_folder / address_list[-1] / "_".join(address_list) + ".yaml"
    """
    nut_name = address_list[-1]
    stem = "_".join(address_list)
    return working_folder / nut_name / f"{stem}.yaml"


# --- Edge Case Tests ---


class TestEdgeCases:
    """Edge case tests for SQLiteDataOperations."""

    def test_empty_dictionary_round_trip(self, tmp_path: Path):
        """Test that an empty dictionary can be stored and retrieved without error.

        Requirements: 11.23
        """
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        data = Dictionary(
            key_def=NutObjectType.STRING,
            value_def=NutObjectType.STRING,
            value={},
        )
        ops.save_data(data, tmp_path, "mynut", filename)
        result = ops.read_data(tmp_path, "mynut", filename)

        assert isinstance(result, Dictionary)
        assert result.key_def == NutObjectType.STRING
        assert result.value_def == NutObjectType.STRING
        assert result.value == {}

    def test_empty_list_round_trip(self, tmp_path: Path):
        """Test that an empty list can be stored and retrieved without error.

        Requirements: 11.24
        """
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        data = ListOfThings(
            value_def=NutObjectType.STRING,
            value=[],
        )
        ops.save_data(data, tmp_path, "mynut", filename)
        result = ops.read_data(tmp_path, "mynut", filename)

        assert isinstance(result, ListOfThings)
        assert result.value_def == NutObjectType.STRING
        assert result.value == []

    def test_none_value_handling_graceful(self, tmp_path: Path):
        """Test that passing None to save_data does not crash.

        The implementation handles None gracefully by storing as a null string.

        Requirements: 11.25
        """
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        # Should not raise any exception
        ops.save_data(None, tmp_path, "mynut", filename)

        # Should be readable without error
        result = ops.read_data(tmp_path, "mynut", filename)
        assert isinstance(result, String)
        assert result.value is None

    def test_overwrite_at_same_address_returns_new_value(self, tmp_path: Path):
        """Test that overwriting at the same address returns the new value.

        Requirements: 11.28
        """
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        ops.save_data(String(value="first"), tmp_path, "mynut", filename)
        ops.save_data(String(value="second"), tmp_path, "mynut", filename)
        result = ops.read_data(tmp_path, "mynut", filename)

        assert isinstance(result, String)
        assert result.value == "second"

    def test_read_from_never_written_address_raises_descriptive_error(self, tmp_path: Path):
        """Test that reading from a never-written address raises a descriptive KeyError.

        Requirements: 11.26
        """
        ops = make_ops(tmp_path)
        address_list = ["never", "written", "address"]
        filename = make_filename(tmp_path, address_list)

        with pytest.raises(KeyError, match="No value stored at address"):
            ops.read_data(tmp_path, "address", filename)

    def test_unsupported_type_raises_value_error_with_descriptive_message(self, tmp_path: Path):
        """Test that passing an unsupported type raises ValueError with a descriptive message.

        Requirements: 11.27
        """
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        # Test with a set (unsupported type)
        with pytest.raises(ValueError, match="Unsupported value type"):
            ops.save_data(set(), tmp_path, "mynut", filename)

        # Test with a custom class instance (unsupported type)
        class CustomUnsupported:
            pass

        with pytest.raises(ValueError, match="Unsupported value type"):
            ops.save_data(CustomUnsupported(), tmp_path, "mynut", filename)
