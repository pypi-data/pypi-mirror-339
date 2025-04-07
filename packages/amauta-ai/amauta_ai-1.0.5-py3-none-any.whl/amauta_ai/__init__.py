"""
AMAUTA - Autonomous Modular Agent for Unified Task Assistance

This package provides a comprehensive set of tools for AI-assisted development,
including task management, code analysis, and documentation generation.
"""

__version__ = "1.0.5"
__author__ = "AMAUTA Team"

# Expose key components at the package level for easier imports
try:
    from amauta_ai.cli import main
    from amauta_ai.imports import initialize_imports

    # Initialize imports on package import
    initialize_imports()

    # Expose the main function for entry points
    __all__ = ["main"]
except ImportError as e:
    import sys
    print(f"Warning: Some imports failed: {e}. AMAUTA may not function correctly until reinstalled.", file=sys.stderr)
    
    # Provide minimal functionality
    __all__ = []

    def main():
        print("AMAUTA initialization failed. Please reinstall the package with: pip install --index-url https://pypi.org/simple/ amauta-ai")
        return 1
