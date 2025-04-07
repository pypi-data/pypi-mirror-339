"""
Exports module for AMAUTA.

This module provides functionality for exporting AMAUTA components 
for external usage or integration.
"""

from amauta_ai.exports.export_manager import ExportManager

# Import key export components with fallbacks
try:
    from amauta_ai.exports.ai import AIExporter
except ImportError:
    import logging
    logging.getLogger(__name__).warning("Failed to import AIExporter")

try:
    from amauta_ai.exports.analyzer import AnalyzerExporter
except ImportError:
    import logging
    logging.getLogger(__name__).warning("Failed to import AnalyzerExporter")

try:
    from amauta_ai.exports.config import ConfigExporter
except ImportError:
    import logging
    logging.getLogger(__name__).warning("Failed to import ConfigExporter")

try:
    from amauta_ai.exports.mcp import MCPExporter
except ImportError:
    import logging
    logging.getLogger(__name__).warning("Failed to import MCPExporter")

try:
    from amauta_ai.exports.rules import RulesExporter
except ImportError:
    import logging
    logging.getLogger(__name__).warning("Failed to import RulesExporter")
    
    class RulesExporter:
        """Fallback Rules Exporter"""
        @staticmethod
        def export_rules(*args, **kwargs):
            return "# Generated Rules (Fallback)\n\n# Rules export failed"

try:
    from amauta_ai.exports.summarizer import SummarizerExporter
except ImportError:
    import logging
    logging.getLogger(__name__).warning("Failed to import SummarizerExporter")

try:
    from amauta_ai.exports.task_manager import TaskManagerExporter
except ImportError:
    import logging
    logging.getLogger(__name__).warning("Failed to import TaskManagerExporter")
