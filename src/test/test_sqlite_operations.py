"""Unit tests for SQLiteDataOperations.

Tests database initialization, primitive save/read, complex type save/read,
and error conditions.
"""

import sqlite3
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


# --- Task 6.1: Test Fixtures ---


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


# --- Task 6.2: Database Initialization Tests ---


class TestDatabaseInitialization:
    """Tests for SQLiteDataOperations database initialization."""

    def test_db_file_created_on_instantiation(self, tmp_path: Path):
        """Test that the SQLite database file is created when instantiated."""
        ops = make_ops(tmp_path)
        db_path = tmp_path / SQLiteDataOperations.DB_FILENAME
        assert db_path.exists()

    def test_nut_values_table_exists(self, tmp_path: Path):
        """Test that the nut_values table is created in the database."""
        ops = make_ops(tmp_path)
        db_path = tmp_path / SQLiteDataOperations.DB_FILENAME
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='nut_values'"
            )
            row = cursor.fetchone()
        finally:
            conn.close()
        assert row is not None
        assert row[0] == "nut_values"

    def test_file_not_found_error_for_missing_folder(self, tmp_path: Path):
        """Test that FileNotFoundError is raised for a non-existent working folder."""
        missing_folder = tmp_path / "does_not_exist"
        with pytest.raises(FileNotFoundError, match="Working folder does not exist"):
            SQLiteDataOperations(working_folder=missing_folder)


# --- Task 6.3: Primitive Save/Read Tests ---


class TestPrimitiveSaveRead:
    """Tests for saving and reading primitive types (String, Integer, FloatingPoint)."""

    def test_save_and_read_string(self, tmp_path: Path):
        """Test save and read for String type."""
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        ops.save_data(String(value="hello"), tmp_path, "mynut", filename)
        result = ops.read_data(tmp_path, "mynut", filename)

        assert isinstance(result, String)
        assert result.value == "hello"
        assert type(result.value) is str

    def test_save_and_read_integer(self, tmp_path: Path):
        """Test save and read for Integer type."""
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        ops.save_data(Integer(value=42), tmp_path, "mynut", filename)
        result = ops.read_data(tmp_path, "mynut", filename)

        assert isinstance(result, Integer)
        assert result.value == 42
        assert type(result.value) is int

    def test_save_and_read_floating_point(self, tmp_path: Path):
        """Test save and read for FloatingPoint type."""
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        ops.save_data(FloatingPoint(value=3.14), tmp_path, "mynut", filename)
        result = ops.read_data(tmp_path, "mynut", filename)

        assert isinstance(result, FloatingPoint)
        assert result.value == 3.14
        assert type(result.value) is float

    def test_type_preservation_int_not_float(self, tmp_path: Path):
        """Verify that an integer value stays int and is not returned as float."""
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        ops.save_data(Integer(value=1), tmp_path, "mynut", filename)
        result = ops.read_data(tmp_path, "mynut", filename)

        assert isinstance(result, Integer)
        assert type(result.value) is int
        assert not isinstance(result.value, float)


# --- Task 6.4: Dictionary and ListOfThings Save/Read Tests ---


class TestComplexTypeSaveRead:
    """Tests for saving and reading Dictionary and ListOfThings types."""

    def test_dict_with_string_keys_and_int_values(self, tmp_path: Path):
        """Test dict with string keys and integer values."""
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        data = Dictionary(
            key_def=NutObjectType.STRING,
            value_def=NutObjectType.INTEGER,
            value={"apple": 1, "banana": 2},
        )
        ops.save_data(data, tmp_path, "mynut", filename)
        result = ops.read_data(tmp_path, "mynut", filename)

        assert isinstance(result, Dictionary)
        assert result.key_def == NutObjectType.STRING
        assert result.value_def == NutObjectType.INTEGER
        assert result.value == {"apple": 1, "banana": 2}

    def test_dict_with_int_keys_and_string_values(self, tmp_path: Path):
        """Test dict with integer keys and string values."""
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        data = Dictionary(
            key_def=NutObjectType.INTEGER,
            value_def=NutObjectType.STRING,
            value={1: "one", 2: "two"},
        )
        ops.save_data(data, tmp_path, "mynut", filename)
        result = ops.read_data(tmp_path, "mynut", filename)

        assert isinstance(result, Dictionary)
        assert result.key_def == NutObjectType.INTEGER
        assert result.value_def == NutObjectType.STRING
        assert result.value == {1: "one", 2: "two"}

    def test_list_with_string_items(self, tmp_path: Path):
        """Test list with string items."""
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        data = ListOfThings(
            value_def=NutObjectType.STRING,
            value=["alpha", "beta", "gamma"],
        )
        ops.save_data(data, tmp_path, "mynut", filename)
        result = ops.read_data(tmp_path, "mynut", filename)

        assert isinstance(result, ListOfThings)
        assert result.value_def == NutObjectType.STRING
        assert result.value == ["alpha", "beta", "gamma"]

    def test_list_with_int_items(self, tmp_path: Path):
        """Test list with integer items."""
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        data = ListOfThings(
            value_def=NutObjectType.INTEGER,
            value=[10, 20, 30],
        )
        ops.save_data(data, tmp_path, "mynut", filename)
        result = ops.read_data(tmp_path, "mynut", filename)

        assert isinstance(result, ListOfThings)
        assert result.value_def == NutObjectType.INTEGER
        assert result.value == [10, 20, 30]


# --- Task 6.5: Error Condition Tests ---


class TestErrorConditions:
    """Tests for error conditions."""

    def test_read_non_existent_address_raises_key_error(self, tmp_path: Path):
        """Test that reading from a non-existent address raises KeyError."""
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        with pytest.raises(KeyError, match="No value stored at address"):
            ops.read_data(tmp_path, "mynut", filename)

    def test_unsupported_type_raises_value_error(self, tmp_path: Path):
        """Test that saving an unsupported type raises ValueError."""
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        with pytest.raises(ValueError, match="Unsupported value type"):
            ops.save_data(object(), tmp_path, "mynut", filename)

    def test_overwrite_at_same_address_returns_new_value(self, tmp_path: Path):
        """Test that overwriting at the same address returns the new value."""
        ops = make_ops(tmp_path)
        address_list = ["attr_db", "parent", "mynut"]
        filename = make_filename(tmp_path, address_list)

        ops.save_data(String(value="first"), tmp_path, "mynut", filename)
        ops.save_data(String(value="second"), tmp_path, "mynut", filename)
        result = ops.read_data(tmp_path, "mynut", filename)

        assert isinstance(result, String)
        assert result.value == "second"
