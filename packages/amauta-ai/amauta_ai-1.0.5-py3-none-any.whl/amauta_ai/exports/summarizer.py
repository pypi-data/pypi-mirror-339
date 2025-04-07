"""
Summarizer module exports for AMAUTA.

This module registers the summarizer components with the export manager.
"""

from amauta_ai.exports.export_manager import (
    ExportManager,
    export_class,
    export_function,
)
from amauta_ai.summarizer.service import SummarizerService, generate_summary

# Get the export manager instance
export_manager = ExportManager()

# Register classes
export_class(SummarizerService)

# Register functions
export_function(generate_summary)

# Register methods from SummarizerService as standalone functions
export_function(SummarizerService.generate_summary)
export_function(SummarizerService._process_file)
export_function(SummarizerService._get_all_files)
export_function(SummarizerService._summarize_content)
export_function(SummarizerService._summarize_python)
export_function(SummarizerService._summarize_js_ts)
