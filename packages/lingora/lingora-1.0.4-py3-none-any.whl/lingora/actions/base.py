"""Base classes for text processing actions."""
from abc import ABC, abstractmethod
from typing import Any

from ..formats.intermediate import Intermediate

class Action(ABC):
    """Base class for text processing actions."""
    
    def __init__(self, intermediate: Intermediate):
        self.intermediate = intermediate
    
    @abstractmethod
    def process(self, content: Any, **kwargs) -> Any:
        """Process the content using the specific action implementation."""
        pass

    def execute(self, content: Any, **kwargs) -> Any:
        """Execute the action using the intermediate format."""
        # Transform to intermediate
        intermediate_content = self.intermediate.transform_to(content)
        
        # Process the content
        processed = self.process(intermediate_content, **kwargs)
        
        # Transform back from intermediate
        return self.intermediate.transform_from(processed)
