"""
Rules module exports for AMAUTA.

This module registers the rules components with the export manager.
"""

from amauta_ai.exports.export_manager import (
    ExportManager,
    export_class,
    export_function,
)
from amauta_ai.rules.generator import RulesGenerator
from amauta_ai.rules.template_manager import RuleTemplate, TemplateManager

# Get the export manager instance
export_manager = ExportManager()

# Register classes
export_class(RulesGenerator)
export_class(TemplateManager)
export_class(RuleTemplate)

# Register methods from RulesGenerator as standalone functions
export_function(RulesGenerator.generate_rules)
export_function(RulesGenerator.save_rules)
export_function(RulesGenerator.generate_and_save_rules)
export_function(RulesGenerator.generate_cursor_rules)
export_function(RulesGenerator.generate_and_save_cursor_rules)
export_function(RulesGenerator.generate_main_cursorrules)
export_function(RulesGenerator.generate_rule_files)

# Register methods from TemplateManager as standalone functions
export_function(TemplateManager.discover_templates)
export_function(TemplateManager.get_templates_by_tag)
export_function(TemplateManager.get_templates_by_tags)
export_function(TemplateManager.get_recommended_templates)
export_function(TemplateManager.merge_templates)
export_function(TemplateManager.apply_template)
