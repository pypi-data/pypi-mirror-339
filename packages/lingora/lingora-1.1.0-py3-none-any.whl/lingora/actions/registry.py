"""Registry for text processing actions."""
from typing import Dict, Type

from .base import Action
from .transliterate import TransliterateAction
from .translate import TranslateAction
from ..formats.intermediate import Intermediate

class ActionRegistry:
    """Registry for managing text processing actions."""
    
    _actions: Dict[str, Type[Action]] = {
        'transliterate': TransliterateAction,
        'translate': TranslateAction,
    }
    
    @classmethod
    def get_action(cls, name: str, intermediate: Intermediate) -> Action:
        """Get an action instance by name."""
        if name not in cls._actions:
            raise ValueError(f"Unknown action: {name}")
        
        action_class = cls._actions[name]
        return action_class(intermediate)
    
    @classmethod
    def register_action(cls, name: str, action_class: Type[Action]) -> None:
        """Register a new action."""
        cls._actions[name] = action_class
