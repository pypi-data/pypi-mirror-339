from .base import TranslationPlugin
from .registry import PluginRegistry
from .openai_plugin import OpenAITranslationPlugin
from .simulator_plugin import SimulatorTranslationPlugin
from .openrouter import OpenRouterPlugin

# Register the plugins
PluginRegistry.register(OpenAITranslationPlugin)
PluginRegistry.register(SimulatorTranslationPlugin)
PluginRegistry.register(OpenRouterPlugin)