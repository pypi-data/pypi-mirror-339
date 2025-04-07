"""
AMAUTA - Autonomous Modular Agent for Unified Task Assistance

This package provides a comprehensive set of tools for AI-assisted development,
including task management, code analysis, and documentation generation.
"""

__version__ = "1.0.13"
__author__ = "AMAUTA Team"

# Expose key components at the package level for easier imports
try:
    # First try to import the integrity checker and run it
    try:
        import importlib
        import logging
        import os
        import sys
        
        # Create missing files if necessary
        for module_name in [
            'amauta_ai.task_manager.template_service',
            'amauta_ai.rules.template_manager'
        ]:
            try:
                importlib.import_module(module_name)
            except ImportError:
                # Try to create the module from fallback
                parts = module_name.split('.')
                if len(parts) >= 3:
                    parent_module = '.'.join(parts[:-1])
                    try:
                        parent = importlib.import_module(parent_module)
                        parent_dir = os.path.dirname(parent.__file__)
                        
                        module_file = f"{parts[-1]}.py"
                        fallback_file = f"{parts[-1]}_fallback.py"
                        
                        module_path = os.path.join(parent_dir, module_file)
                        fallback_path = os.path.join(parent_dir, fallback_file)
                        
                        if os.path.exists(fallback_path) and not os.path.exists(module_path):
                            print(f"Creating {module_path} from {fallback_path}")
                            with open(fallback_path, 'r') as src:
                                with open(module_path, 'w') as dst:
                                    dst.write(src.read())
                    except Exception as e:
                        print(f"Failed to create module {module_name}: {e}")
        
        # Apply perplexipy timeout patch if available
        try:
            from amauta_ai.utils.fix_perplexity import patch_perplexipy
            # Only attempt to patch if perplexipy is installed
            if importlib.util.find_spec("perplexipy") is not None:
                patch_perplexipy()
        except Exception as e:
            print(f"Warning: Failed to apply perplexipy timeout patch: {e}")
            
        from amauta_ai.cli import main
        from amauta_ai.imports import initialize_imports

        # Initialize imports on package import
        initialize_imports()

        # Expose the main function for entry points
        __all__ = ["main"]
    except ImportError as e:
        print(f"Error during integrity check: {e}")
        raise
except ImportError as e:
    import sys
    print(f"Warning: Some imports failed: {e}. AMAUTA may not function correctly until reinstalled.", file=sys.stderr)
    
    # Provide minimal functionality
    __all__ = []

    def main():
        print("AMAUTA initialization failed. Please reinstall the package with: pip install --index-url https://pypi.org/simple/ amauta-ai==1.0.7")
        return 1
