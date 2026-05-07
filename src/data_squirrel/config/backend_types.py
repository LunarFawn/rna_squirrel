"""Backend type definitions and data operations protocol for data_squirrel."""

from enum import Enum
from typing import Protocol, Any
from pathlib import Path


class BackendType(Enum):
    """Enum representing the available persistence backends."""

    YAML = "YAML"
    SQLITE = "SQLITE"


class DataOperationsProtocol(Protocol):
    """Protocol defining the interface contract for persistence backends.

    Both YamlDataOperations and SQLiteDataOperations must satisfy this interface.
    """

    def save_data(
        self, data: Any, working_folder: Path, nut_name: str, filename: Path
    ) -> None:
        """Persist a typed data object (String, Integer, FloatingPoint, Dictionary, ListOfThings, or dataclass fields)."""
        ...

    def read_data(self, working_folder: Path, nut_name: str, filename: Path) -> Any:
        """Read and return a typed data object from storage."""
        ...
