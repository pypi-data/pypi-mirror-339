"""Base classes for format handlers."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Union


class FormatHandler(ABC):
    """Base class for format handlers."""

    @abstractmethod
    def read(self, input_path: Path) -> Any:
        """Read content from a file."""
        pass

    @abstractmethod
    def write(self, content: Any, output_path: Path) -> None:
        """Write content to a file."""
        pass

    @abstractmethod
    def validate(self, content: Any) -> bool:
        """Validate content format."""
        pass
