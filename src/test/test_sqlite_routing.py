"""Integration tests for the full SQLite routing pipeline.

Tests the complete flow: CustomAttribute set → NutFilterDefinitions → SQLiteDataOperations → storage,
and the reverse for reads.

Requirements: 11.15, 11.16, 11.17, 11.18
"""

import pytest
from enum import Enum
from pathlib import Path
from typing import Any

from data_squirrel.config.dynamic_data_nut import Nut, CustomAttribute
from data_squirrel.config.nut_yaml_objects import AtrClass, GenericAttribute
from data_squirrel.config.backend_types import BackendType


class NutAttributes(Enum):
    """Enum for test attribute sections. Values must end with _db for routing."""
    SECTION_A = "section_a_db"


class MultiNutAttributes(Enum):
    """Enum with multiple sections for multi-attribute tests."""
    SECTION_A = "section_a_db"
    SECTION_B = "section_b_db"


class SimpleTestNut(Nut):
    """Subclass of Nut for testing. Subclassing gives us __dict__ for dynamic attrs."""

    def __init__(self, working_folder: Path, var_name: str, backend_type: BackendType = BackendType.SQLITE):
        super().__init__(
            enum_list=NutAttributes,
            use_db=True,
            db=None,
            var_name=var_name,
            working_folder=working_folder,
            backend_type=backend_type,
        )


class MultiSectionTestNut(Nut):
    """Subclass of Nut with multiple sections for testing."""

    def __init__(self, working_folder: Path, var_name: str, backend_type: BackendType = BackendType.SQLITE):
        super().__init__(
            enum_list=MultiNutAttributes,
            use_db=True,
            db=None,
            var_name=var_name,
            working_folder=working_folder,
            backend_type=backend_type,
        )


@pytest.fixture
def sqlite_nut(tmp_path: Path) -> SimpleTestNut:
    """Create a Nut instance with SQLite backend for testing."""
    nut = SimpleTestNut(working_folder=tmp_path, var_name="test_nut")
    # Add a child attribute for string values
    nut.section_a_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=str, attribute="name_db"))
    return nut


@pytest.fixture
def multi_section_nut(tmp_path: Path) -> MultiSectionTestNut:
    """Create a Nut with multiple sections for distinct address testing."""
    nut = MultiSectionTestNut(working_folder=tmp_path, var_name="multi_nut")
    nut.section_a_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=str, attribute="value_one_db"))
    nut.section_a_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=str, attribute="value_two_db"))
    nut.section_b_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=str, attribute="value_one_db"))
    return nut


class TestStringRoundTrip:
    """Test string values through the full pipeline."""

    def test_string_set_and_get(self, sqlite_nut: SimpleTestNut):
        """Test that a string value survives the full outbound/inbound pipeline."""
        sqlite_nut.section_a_db.name_db = "hello world"
        result = sqlite_nut.section_a_db.name_db
        assert result == "hello world"
        assert type(result) is str


class TestIntegerRoundTrip:
    """Test integer values through the full pipeline."""

    def test_integer_set_and_get(self, tmp_path: Path):
        """Test that an integer value survives the full outbound/inbound pipeline."""
        nut = SimpleTestNut(working_folder=tmp_path, var_name="int_nut")
        nut.section_a_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=int, attribute="count_db"))
        nut.section_a_db.count_db = 42
        result = nut.section_a_db.count_db
        assert result == 42
        assert type(result) is int


class TestFloatRoundTrip:
    """Test float values through the full pipeline."""

    def test_float_set_and_get(self, tmp_path: Path):
        """Test that a float value survives the full outbound/inbound pipeline."""
        nut = SimpleTestNut(working_folder=tmp_path, var_name="float_nut")
        nut.section_a_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=float, attribute="score_db"))
        nut.section_a_db.score_db = 3.14
        result = nut.section_a_db.score_db
        assert result == 3.14
        assert type(result) is float


class TestDictRoundTrip:
    """Test dictionary values through the full pipeline."""

    def test_dict_set_and_get(self, tmp_path: Path):
        """Test that a dict value survives the full outbound/inbound pipeline."""
        nut = SimpleTestNut(working_folder=tmp_path, var_name="dict_nut")
        nut.section_a_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=dict, attribute="mapping_db"))
        test_dict = {"apple": 1, "banana": 2, "cherry": 3}
        nut.section_a_db.mapping_db = test_dict
        result = nut.section_a_db.mapping_db
        assert result == test_dict
        assert type(result) is dict


class TestListRoundTrip:
    """Test list values through the full pipeline."""

    def test_list_set_and_get(self, tmp_path: Path):
        """Test that a list value survives the full outbound/inbound pipeline."""
        nut = SimpleTestNut(working_folder=tmp_path, var_name="list_nut")
        nut.section_a_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=list, attribute="items_db"))
        test_list = ["alpha", "beta", "gamma"]
        nut.section_a_db.items_db = test_list
        result = nut.section_a_db.items_db
        assert result == test_list
        assert type(result) is list


class TestMultipleAttributes:
    """Test multiple attributes stored at distinct addresses."""

    def test_multiple_attrs_same_section(self, multi_section_nut: MultiSectionTestNut):
        """Test that multiple attributes in the same section are stored independently."""
        multi_section_nut.section_a_db.value_one_db = "first"
        multi_section_nut.section_a_db.value_two_db = "second"

        assert multi_section_nut.section_a_db.value_one_db == "first"
        assert multi_section_nut.section_a_db.value_two_db == "second"

    def test_multiple_attrs_different_sections(self, multi_section_nut: MultiSectionTestNut):
        """Test that attributes in different sections are stored independently."""
        multi_section_nut.section_a_db.value_one_db = "from_a"
        multi_section_nut.section_b_db.value_one_db = "from_b"

        assert multi_section_nut.section_a_db.value_one_db == "from_a"
        assert multi_section_nut.section_b_db.value_one_db == "from_b"
