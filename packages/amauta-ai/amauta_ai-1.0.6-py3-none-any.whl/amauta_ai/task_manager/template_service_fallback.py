"""
Fallback implementation of template_service.py for deployment.
"""

class TemplateService:
    """
    Fallback Template Service for managing task templates.
    This implementation provides basic functionality when the real implementation is missing.
    """
    
    def __init__(self, config_path=None):
        """Initialize the Template Service with a config path."""
        self.templates = {}
        self.config_path = config_path or ".amautarc.yaml"
        print("Using fallback TemplateService implementation")
    
    def get_template(self, template_id):
        """Get a task template by ID."""
        return self.templates.get(template_id)
    
    def list_templates(self):
        """List all available templates."""
        return list(self.templates.values())
    
    def add_template(self, template):
        """Add a new template."""
        self.templates[template["id"]] = template
        return template
    
    def update_template(self, template_id, template_data):
        """Update an existing template."""
        if template_id in self.templates:
            self.templates[template_id].update(template_data)
            return self.templates[template_id]
        return None
    
    def delete_template(self, template_id):
        """Delete a template."""
        if template_id in self.templates:
            return self.templates.pop(template_id)
        return None 