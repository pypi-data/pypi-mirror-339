"""
Rules module for AMAUTA.

This module provides functionality for generating and managing Cursor rules.
"""

# Import generator safely
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

# Import template manager (with fallback)
try:
    try:
        # First try the original module
        from amauta_ai.rules.template_manager import TemplateManager
    except ImportError:
        # Try the fallback module
        try:
            import os
            import sys
            
            # Create the template_manager.py from fallback if needed
            current_dir = os.path.dirname(__file__)
            template_manager_path = os.path.join(current_dir, 'template_manager.py')
            fallback_path = os.path.join(current_dir, 'template_manager_fallback.py')
            
            if not os.path.exists(template_manager_path) and os.path.exists(fallback_path):
                print(f"Creating {template_manager_path} from {fallback_path}")
                with open(fallback_path, 'r') as src:
                    with open(template_manager_path, 'w') as dst:
                        dst.write(src.read())
                
            # Now try to import again
            from amauta_ai.rules.template_manager import TemplateManager
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Failed to create template_manager.py: {e}")
            
            # Provide a minimal fallback
            class TemplateManager:
                """Minimal fallback for TemplateManager"""
                def __init__(self, *args, **kwargs):
                    self.templates = {}
                
                def generate_cursor_rules(self, *args, **kwargs):
                    return "# Generated Cursor Rules\n\n# This is a minimal fallback implementation"
except Exception as e:
    import logging
    logging.getLogger(__name__).error(f"Failed to import or create TemplateManager: {e}")
    
    # Provide a minimal fallback
    class TemplateManager:
        """Minimal fallback for TemplateManager"""
        def __init__(self, *args, **kwargs):
            self.templates = {}
        
        def generate_cursor_rules(self, *args, **kwargs):
            return "# Generated Cursor Rules\n\n# This is a minimal fallback implementation"

__all__ = [
    "RulesGenerator",
    "TemplateManager"
]
