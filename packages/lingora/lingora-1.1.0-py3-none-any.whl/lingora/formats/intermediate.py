"""Base classes for intermediate format handling."""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, TypeVar, List, Union

T = TypeVar('T')

class Intermediate(ABC):
    """Base class for intermediate formats."""
    
    @abstractmethod
    def transform_to(self, content: Any, chunk_size: int) -> T:
        """Transform content from source format to intermediate format."""
        pass
    
    @abstractmethod
    def transform_from(self, content: T) -> Any:
        """Transform content from intermediate format back to source format."""
        pass

    @abstractmethod
    def read(self, path: Union[str, Path]) -> Any:
        """Read content from a file."""
        pass

    @abstractmethod
    def read_recursive(self, directory: Union[str, Path]) -> List[Any]:
        """Read content from all matching files in a directory recursively."""
        pass

    @abstractmethod
    def process(self, content: Any, chunk_size: int) -> str:
        """Process content in chunks."""
        pass

    @abstractmethod
    def write(self, content: Any, path: Union[str, Path], debug: bool = False) -> None:
        """Write content to a file."""
        pass

    @abstractmethod
    def write_recursive(self, contents: List[Any], directory: Union[str, Path], debug: bool = False) -> None:
        """Write multiple UI strings to files in a directory recursively."""
        pass
