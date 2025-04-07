"""
AMAUTA - Autonomous Modular Agent for Unified Task Assistance

This package provides a comprehensive set of tools for AI-assisted development,
including task management, code analysis, and documentation generation.
"""

__version__ = "1.0.4"
__author__ = "AMAUTA Team"

# Expose key components at the package level for easier imports
from amauta_ai.cli import main
from amauta_ai.imports import initialize_imports

# Initialize imports on package import
initialize_imports()

# Expose the main function for entry points
__all__ = ["main"]

# Import main app for easier access
