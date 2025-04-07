"""
Rules module for AMAUTA.

This module provides functionality for generating rules for various IDEs and environments.
"""

from amauta_ai.rules.generator import *
from amauta_ai.rules.template_manager import *

__all__ = [
    "RulesGenerator",
    "generate_rules",
    "save_rules",
    "generate_and_save_rules",
    "generate_cursor_rules",
    "generate_and_save_cursor_rules",
    "RuleTemplate",
    "TemplateManager",
]
