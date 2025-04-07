"""
Main module entry point for AMAUTA.

This allows running the application directly with:
python -m amauta_ai
"""

import sys

from amauta_ai.main import app

if __name__ == "__main__":
    # Ensure imports are initialized
    from amauta_ai.imports import initialize_imports

    initialize_imports()

    # Run the main application
    sys.exit(app())
