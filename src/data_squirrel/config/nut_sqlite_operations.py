"""SQLite persistence backend for data_squirrel."""

import sqlite3
import json
import dataclasses
import importlib
from pathlib import Path
from typing import Any, Dict, List


from data_squirrel.config.nut_yaml_objects import (
    String,
    Integer,
    FloatingPoint,
    Dictionary,
    ListOfThings,
    NutObjectType,
)


class SQLiteDataOperations:
    """SQLite-based persistence backend for storing typed attribute values.

    Uses a single SQLite database file per working folder. Values are stored
    in a flat table keyed by the address path derived from the attribute hierarchy.
    """

    DB_FILENAME = "nut_data.db"

    def __init__(self, working_folder: Path) -> None:
        if not working_folder.exists():
            raise FileNotFoundError(
                f"Working folder does not exist: {working_folder}"
            )
        self._working_folder = working_folder
        self._db_path = working_folder / self.DB_FILENAME
        self._init_db()

    def _init_db(self) -> None:
        """Create the nut_values table if it does not already exist."""
        conn = sqlite3.connect(self._db_path)
        try:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS nut_values (
                    address_key TEXT PRIMARY KEY,
                    value_type  TEXT NOT NULL,
                    value_data  TEXT NOT NULL,
                    nut_name    TEXT NOT NULL
                )
                """
            )
            conn.commit()
        finally:
            conn.close()

    def _make_address_key(self, address_list: List[str]) -> str:
        """Join address list components with '|' separator to form the storage key."""
        return "|".join(address_list)

    def _extract_address_from_filename(self, filename: Path) -> List[str]:
        """Derive the address list from the filename Path parameter.

        The filename is constructed as:
            working_folder / address_list[-1] / "_".join(address_list) + ".yaml"

        So the stem (filename without extension) is the address list joined by '_'.
        We split on '_' to recover the original address components.
        """
        return filename.stem.split("_")

    def save_data(
        self, data: Any, working_folder: Path, nut_name: str, filename: Path
    ) -> None:
        """Persist typed data to SQLite.

        Handles String, Integer, FloatingPoint, Dictionary, ListOfThings,
        and dataclass instances.
        """
        address_list = self._extract_address_from_filename(filename)
        address_key = self._make_address_key(address_list)

        if isinstance(data, String):
            value_type = "STRING"
            value_data = json.dumps({"value": data.value})
        elif isinstance(data, Integer):
            value_type = "INTEGER"
            value_data = json.dumps({"value": data.value})
        elif isinstance(data, FloatingPoint):
            value_type = "FLOAT"
            value_data = json.dumps({"value": data.value})
        elif isinstance(data, Dictionary):
            value_type = "DICTIONARY"
            value_data = json.dumps({
                "key_def": data.key_def.name,
                "value_def": data.value_def.name,
                "value": data.value,
            })
        elif isinstance(data, ListOfThings):
            value_type = "LIST"
            value_data = json.dumps({
                "value_def": data.value_def.name,
                "value": data.value,
            })
        elif dataclasses.is_dataclass(data) and not isinstance(data, type):
            value_type = "DATACLASS"
            cls = type(data)
            module = cls.__module__
            attribute = cls.__qualname__
            fields_data: Dict[str, Any] = {}
            for f in dataclasses.fields(data):
                field_value = getattr(data, f.name)
                if isinstance(field_value, str):
                    fields_data[f.name] = {"type": "STRING", "value": field_value}
                elif isinstance(field_value, int):
                    fields_data[f.name] = {"type": "INTEGER", "value": field_value}
                elif isinstance(field_value, float):
                    fields_data[f.name] = {"type": "FLOAT", "value": field_value}
                else:
                    fields_data[f.name] = {"type": "STRING", "value": str(field_value)}
            value_data = json.dumps({
                "module": module,
                "attribute": attribute,
                "fields": fields_data,
            })
        elif data is None:
            # Gracefully handle None - store as a null string value
            value_type = "STRING"
            value_data = json.dumps({"value": None})
        else:
            raise ValueError(
                f"Unsupported value type: {type(data)}. Please update and try again."
            )

        conn = sqlite3.connect(self._db_path)
        try:
            conn.execute(
                """
                INSERT OR REPLACE INTO nut_values (address_key, value_type, value_data, nut_name)
                VALUES (?, ?, ?, ?)
                """,
                (address_key, value_type, value_data, nut_name),
            )
            conn.commit()
        finally:
            conn.close()

    def read_data(
        self, working_folder: Path, nut_name: str, filename: Path
    ) -> Any:
        """Read typed data from SQLite.

        Returns String, Integer, FloatingPoint, Dictionary, ListOfThings,
        or reconstructed dataclass instances.
        """
        address_list = self._extract_address_from_filename(filename)
        address_key = self._make_address_key(address_list)

        conn = sqlite3.connect(self._db_path)
        try:
            cursor = conn.execute(
                "SELECT value_type, value_data FROM nut_values WHERE address_key = ?",
                (address_key,),
            )
            row = cursor.fetchone()
        finally:
            conn.close()

        if row is None:
            raise KeyError(f"No value stored at address: {address_key}")

        value_type, value_data_str = row
        payload = json.loads(value_data_str)

        if value_type == "STRING":
            return String(value=payload["value"])
        elif value_type == "INTEGER":
            return Integer(value=payload["value"])
        elif value_type == "FLOAT":
            return FloatingPoint(value=payload["value"])
        elif value_type == "DICTIONARY":
            key_def = NutObjectType[payload["key_def"]]
            value_def = NutObjectType[payload["value_def"]]
            raw_dict = payload["value"]
            # Cast keys back to proper types (JSON only supports string keys)
            typed_dict: Dict[Any, Any] = {}
            for k, v in raw_dict.items():
                typed_key = self._cast_value(k, key_def)
                typed_dict[typed_key] = v
            return Dictionary(key_def=key_def, value_def=value_def, value=typed_dict)
        elif value_type == "LIST":
            value_def = NutObjectType[payload["value_def"]]
            return ListOfThings(value_def=value_def, value=payload["value"])
        elif value_type == "DATACLASS":
            module_path = payload["module"]
            attribute_name = payload["attribute"]
            fields_data = payload["fields"]
            # Import the class
            mod = importlib.import_module(module_path)
            cls = getattr(mod, attribute_name)
            # Reconstruct field values
            kwargs: Dict[str, Any] = {}
            for field_name, field_info in fields_data.items():
                field_type = field_info["type"]
                field_value = field_info["value"]
                if field_type == "INTEGER":
                    kwargs[field_name] = int(field_value)
                elif field_type == "FLOAT":
                    kwargs[field_name] = float(field_value)
                else:
                    kwargs[field_name] = field_value
            return cls(**kwargs)
        else:
            raise ValueError(f"Unknown value_type in database: {value_type}")

    def _cast_value(self, value: Any, type_def: NutObjectType) -> Any:
        """Cast a value to the appropriate Python type based on NutObjectType."""
        if type_def == NutObjectType.STRING:
            return str(value)
        elif type_def == NutObjectType.INTEGER:
            return int(value)
        elif type_def == NutObjectType.FLOATINGPOINT:
            return float(value)
        else:
            return value
