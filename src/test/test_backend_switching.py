"""Integration tests for BackendType enum switching.

Tests that YAML and SQLITE backends produce equivalent results for the same operations.

Requirements: 11.19, 11.20, 11.21, 11.22
"""

import pytest
from enum import Enum
from pathlib import Path

from data_squirrel.config.dynamic_data_nut import Nut, CustomAttribute
from data_squirrel.config.nut_yaml_objects import AtrClass, GenericAttribute
from data_squirrel.config.backend_types import BackendType
from data_squirrel.config.nut_data_manager import init_variable_folder


class SwitchAttributes(Enum):
    """Enum for backend switching tests. Values must end with _db."""
    DATA = "data_db"


class YamlTestNut(Nut):
    """Subclass of Nut for YAML backend testing."""

    def __init__(self, working_folder: Path, var_name: str):
        super().__init__(
            enum_list=SwitchAttributes,
            use_db=True,
            db=None,
            var_name=var_name,
            working_folder=working_folder,
            backend_type=BackendType.YAML,
        )


class SqliteTestNut(Nut):
    """Subclass of Nut for SQLite backend testing."""

    def __init__(self, working_folder: Path, var_name: str):
        super().__init__(
            enum_list=SwitchAttributes,
            use_db=True,
            db=None,
            var_name=var_name,
            working_folder=working_folder,
            backend_type=BackendType.SQLITE,
        )


@pytest.mark.slow
class TestBackendEquivalenceString:
    """Test that YAML and SQLITE backends produce equivalent results for strings."""

    def test_string_equivalence(self, tmp_path: Path):
        """Both backends should produce the same result for a string value."""
        # YAML backend
        yaml_path = tmp_path / "yaml_workspace"
        yaml_path.mkdir()
        yaml_nut = YamlTestNut(working_folder=yaml_path, var_name="yaml_nut")
        yaml_nut.data_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=str, attribute="name_db"))
        yaml_nut.data_db.name_db = "hello"
        yaml_result = yaml_nut.data_db.name_db

        # SQLite backend
        sqlite_path = tmp_path / "sqlite_workspace"
        sqlite_path.mkdir()
        sqlite_nut = SqliteTestNut(working_folder=sqlite_path, var_name="sqlite_nut")
        sqlite_nut.data_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=str, attribute="name_db"))
        sqlite_nut.data_db.name_db = "hello"
        sqlite_result = sqlite_nut.data_db.name_db

        assert yaml_result == sqlite_result
        assert type(yaml_result) is type(sqlite_result)


@pytest.mark.slow
class TestBackendEquivalenceInt:
    """Test that YAML and SQLITE backends produce equivalent results for integers."""

    def test_int_equivalence(self, tmp_path: Path):
        """Both backends should produce the same result for an integer value."""
        # YAML backend
        yaml_path = tmp_path / "yaml_workspace"
        yaml_path.mkdir()
        yaml_nut = YamlTestNut(working_folder=yaml_path, var_name="yaml_nut")
        yaml_nut.data_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=int, attribute="count_db"))
        yaml_nut.data_db.count_db = 99
        yaml_result = yaml_nut.data_db.count_db

        # SQLite backend
        sqlite_path = tmp_path / "sqlite_workspace"
        sqlite_path.mkdir()
        sqlite_nut = SqliteTestNut(working_folder=sqlite_path, var_name="sqlite_nut")
        sqlite_nut.data_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=int, attribute="count_db"))
        sqlite_nut.data_db.count_db = 99
        sqlite_result = sqlite_nut.data_db.count_db

        assert yaml_result == sqlite_result
        assert type(yaml_result) is type(sqlite_result)


@pytest.mark.slow
class TestBackendEquivalenceFloat:
    """Test that YAML and SQLITE backends produce equivalent results for floats."""

    def test_float_equivalence(self, tmp_path: Path):
        """Both backends should produce the same result for a float value.

        Note: YAML backend returns ruamel.yaml ScalarFloat (a float subclass),
        so we check isinstance(float) rather than exact type identity.
        """
        # YAML backend
        yaml_path = tmp_path / "yaml_workspace"
        yaml_path.mkdir()
        yaml_nut = YamlTestNut(working_folder=yaml_path, var_name="yaml_nut")
        yaml_nut.data_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=float, attribute="score_db"))
        yaml_nut.data_db.score_db = 2.718
        yaml_result = yaml_nut.data_db.score_db

        # SQLite backend
        sqlite_path = tmp_path / "sqlite_workspace"
        sqlite_path.mkdir()
        sqlite_nut = SqliteTestNut(working_folder=sqlite_path, var_name="sqlite_nut")
        sqlite_nut.data_db.new_attr(GenericAttribute(atr_class=AtrClass.CHILD, atr_type=float, attribute="score_db"))
        sqlite_nut.data_db.score_db = 2.718
        sqlite_result = sqlite_nut.data_db.score_db

        assert yaml_result == sqlite_result
        assert isinstance(yaml_result, float)
        assert isinstance(sqlite_result, float)
