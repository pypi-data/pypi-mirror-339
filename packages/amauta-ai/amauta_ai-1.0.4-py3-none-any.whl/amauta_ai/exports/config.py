"""
Config module exports for AMAUTA.

This module registers the config components with the export manager.
"""

from amauta_ai.config.env_manager import EnvManager
from amauta_ai.config.models import (
    AiProviderConfig,
    AiProviderType,
    AmautarcConfig,
    AnalyzerConfig,
    ProjectConfig,
)
from amauta_ai.config.service import ConfigService
from amauta_ai.exports.export_manager import (
    ExportManager,
    export_class,
    export_function,
)

# Get the export manager instance
export_manager = ExportManager()

# Register classes
export_class(ConfigService)
export_class(AmautarcConfig)
export_class(AiProviderType)
export_class(AiProviderConfig)
export_class(AnalyzerConfig)
export_class(ProjectConfig)
export_class(EnvManager)

# Register methods from ConfigService as standalone functions
export_function(ConfigService.get_config)
export_function(ConfigService.get_api_key)
export_function(ConfigService.save_config)
export_function(ConfigService.generate_env_example)
export_function(ConfigService.generate_amautarc_example)
export_function(ConfigService.get_anthropic_config)
export_function(ConfigService.get_perplexity_config)
export_function(ConfigService.get_provider_config)
export_function(ConfigService.get_provider_preferences)
export_function(ConfigService.get_provider_capabilities)
export_function(ConfigService.select_provider)

# Register methods from EnvManager as standalone functions
export_function(EnvManager.load)
export_function(EnvManager.get)
export_function(EnvManager.set)
export_function(EnvManager.get_int)
export_function(EnvManager.get_bool)
export_function(EnvManager.get_float)
export_function(EnvManager.get_list)
export_function(EnvManager.save)
export_function(EnvManager.generate_example)

# Initialize services
config_service = ConfigService()
