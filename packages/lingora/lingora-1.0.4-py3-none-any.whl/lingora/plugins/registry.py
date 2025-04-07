from typing import Dict, Type, Optional
from .base import TranslationPlugin

class PluginRegistry:
    """Registry for managing translation plugins."""
    
    _plugins: Dict[str, Type[TranslationPlugin]] = {}
    
    @classmethod
    def register(cls, plugin_class: Type[TranslationPlugin]) -> None:
        """Register a new plugin class."""
        plugin = plugin_class()
        cls._plugins[plugin.get_name()] = plugin_class
    
    @classmethod
    def get_plugin(cls, name: str) -> Optional[TranslationPlugin]:
        """Get a plugin instance by name."""
        plugin_class = cls._plugins.get(name)
        if plugin_class:
            return plugin_class()
        return None
    
    @classmethod
    def get_available_plugins(cls) -> list[str]:
        """Get list of available plugin names."""
        return list(cls._plugins.keys())
    
    @classmethod
    def clear(cls) -> None:
        """Clear all registered plugins."""
        cls._plugins.clear() 