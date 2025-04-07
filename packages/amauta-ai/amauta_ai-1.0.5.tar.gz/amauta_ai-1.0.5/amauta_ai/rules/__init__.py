"""
Rules module for AMAUTA.

This module provides functionality for generating and managing Cursor rules.
"""

from amauta_ai.rules.generator import RulesGenerator

# Import template manager with fallback
try:
    from amauta_ai.rules.template_manager import TemplateManager
except ImportError:
    try:
        from amauta_ai.rules.template_manager_fallback import TemplateManager
        import logging
        logging.getLogger(__name__).warning("Using fallback TemplateManager")
    except ImportError:
        import logging
        logging.getLogger(__name__).error("Failed to import TemplateManager and fallback")
        
        class TemplateManager:
            """Minimal stub for TemplateManager when not available"""
            def __init__(self, *args, **kwargs):
                self.templates = {}
            
            def generate_cursor_rules(self, *args, **kwargs):
                return "# Generated Cursor Rules\n\n# This is a minimal stub implementation"

__all__ = [
    "RulesGenerator",
    "TemplateManager"
]
