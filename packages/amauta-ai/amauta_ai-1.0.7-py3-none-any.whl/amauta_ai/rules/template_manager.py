"""
Fallback implementation of template_manager.py for deployment.
"""

class TemplateManager:
    """
    Fallback Template Manager for rules management.
    This implementation provides basic functionality when the real implementation is missing.
    """
    
    def __init__(self, config_path=None):
        """Initialize the Template Manager with a config path."""
        self.templates = {}
        self.config_path = config_path or ".amautarc.yaml"
        print("Using fallback TemplateManager implementation")
    
    def get_template(self, template_id):
        """Get a rule template by ID."""
        return self.templates.get(template_id)
    
    def list_templates(self):
        """List all available templates."""
        return list(self.templates.values())
    
    def apply_template(self, template_id, context=None):
        """Apply a template with the given context."""
        template = self.get_template(template_id)
        if not template:
            return None
        return template
    
    def generate_cursor_rules(self, context=None):
        """Generate Cursor rules based on analysis."""
        return "# Generated Cursor Rules\n\n# This is a fallback implementation" 