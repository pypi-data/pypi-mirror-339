"""
Rules exporter module.

This module provides functionality for exporting rules to various formats.
"""

# Try importing the main modules first
try:
    from amauta_ai.rules.generator import RulesGenerator
except ImportError as e:
    import logging
    logging.getLogger(__name__).warning(f"Failed to import RulesGenerator: {e}")
    
    # Minimal fallback
    class RulesGenerator:
        """Minimal fallback for RulesGenerator"""
        def __init__(self, *args, **kwargs):
            pass
        
        def generate_rules(self, *args, **kwargs):
            return "# Generated Rules\n\n# This is a minimal fallback implementation"

try:
    from amauta_ai.rules.template_manager import TemplateManager
except ImportError as e:
    import logging
    logging.getLogger(__name__).warning(f"Failed to import TemplateManager: {e}")
    
    # Minimal fallback
    class TemplateManager:
        """Minimal fallback for TemplateManager"""
        def __init__(self, *args, **kwargs):
            self.templates = {}
        
        def generate_cursor_rules(self, *args, **kwargs):
            return "# Generated Cursor Rules\n\n# This is a minimal fallback implementation"


class RulesExporter:
    """
    Exports rules for various IDEs and environments.
    """
    
    @staticmethod
    def export_rules(format="cursor", context=None):
        """
        Export rules in the specified format.
        
        Args:
            format (str): The format to export rules in (default: "cursor")
            context (dict): Context data for rule generation
            
        Returns:
            str: The exported rules content
        """
        try:
            if format == "cursor":
                template_manager = TemplateManager()
                return template_manager.generate_cursor_rules(context)
            else:
                # Use rules generator for other formats
                generator = RulesGenerator()
                return generator.generate_rules(format, context)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Error exporting rules: {e}")
            return f"# Failed to export rules\n# Error: {e}"
