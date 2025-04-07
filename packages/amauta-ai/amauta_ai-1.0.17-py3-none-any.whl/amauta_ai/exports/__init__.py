"""
Exports module for AMAUTA.

This module provides functionality for exporting AMAUTA components 
for external usage or integration.
"""

import importlib
import logging
import sys
from typing import Optional, Any, Dict, Callable, Type, List, TypeVar

logger = logging.getLogger(__name__)

# Import the export manager first since it's not dependent on other modules
from amauta_ai.exports.export_manager import ExportManager
export_manager = ExportManager.get_instance()

# Define lazy loaders for exporters to avoid circular imports
def _lazy_import(module_path: str, class_name: str) -> Optional[Any]:
    """Lazily import a class from a module path."""
    try:
        module = importlib.import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        logger.warning(f"Failed to import {class_name}: {str(e)}")
        return None

# Lazy load exporters
def get_ai_exporter() -> Any:
    """Get the AI exporter instance."""
    exporter = _lazy_import("amauta_ai.exports.ai", "AIExporter") 
    if exporter is None:
        logger.warning("Using fallback AIExporter")
        # Define a minimal fallback exporter
        class FallbackAIExporter:
            @staticmethod
            def export_ai(*args, **kwargs):
                return "# AI Export Failed\n\nFallback AIExporter used."
        return FallbackAIExporter
    return exporter

def get_analyzer_exporter() -> Any:
    """Get the Analyzer exporter instance."""
    exporter = _lazy_import("amauta_ai.exports.analyzer", "AnalyzerExporter")
    if exporter is None:
        logger.warning("Using fallback AnalyzerExporter")
        # Define a minimal fallback exporter
        class FallbackAnalyzerExporter:
            @staticmethod
            def export_analyzer(*args, **kwargs):
                return "# Analyzer Export Failed\n\nFallback AnalyzerExporter used."
        return FallbackAnalyzerExporter
    return exporter

def get_config_exporter() -> Any:
    """Get the Config exporter instance."""
    exporter = _lazy_import("amauta_ai.exports.config", "ConfigExporter")
    if exporter is None:
        logger.warning("Using fallback ConfigExporter")
        # Define a minimal fallback exporter
        class FallbackConfigExporter:
            @staticmethod
            def export_config(*args, **kwargs):
                return "# Config Export Failed\n\nFallback ConfigExporter used."
        return FallbackConfigExporter
    return exporter

def get_mcp_exporter() -> Any:
    """Get the MCP exporter instance."""
    exporter = _lazy_import("amauta_ai.exports.mcp", "MCPExporter")
    if exporter is None:
        logger.warning("Using fallback MCPExporter")
        # Define a minimal fallback exporter
        class FallbackMCPExporter:
            @staticmethod
            def export_mcp(*args, **kwargs):
                return "# MCP Export Failed\n\nFallback MCPExporter used."
        return FallbackMCPExporter
    return exporter

def get_summarizer_exporter() -> Any:
    """Get the Summarizer exporter instance."""
    exporter = _lazy_import("amauta_ai.exports.summarizer", "SummarizerExporter")
    if exporter is None:
        logger.warning("Using fallback SummarizerExporter")
        # Define a minimal fallback exporter
        class FallbackSummarizerExporter:
            @staticmethod
            def export_summarizer(*args, **kwargs):
                return "# Summarizer Export Failed\n\nFallback SummarizerExporter used."
        return FallbackSummarizerExporter
    return exporter

def get_task_manager_exporter() -> Any:
    """Get the TaskManager exporter instance."""
    exporter = _lazy_import("amauta_ai.exports.task_manager", "TaskManagerExporter")
    if exporter is None:
        logger.warning("Using fallback TaskManagerExporter")
        # Define a minimal fallback exporter
        class FallbackTaskManagerExporter:
            @staticmethod
            def export_task_manager(*args, **kwargs):
                return "# TaskManager Export Failed\n\nFallback TaskManagerExporter used."
        return FallbackTaskManagerExporter
    return exporter

def get_rules_exporter() -> Any:
    """Get the Rules exporter instance."""
    exporter = _lazy_import("amauta_ai.exports.rules", "RulesExporter")
    if exporter is None:
        logger.warning("Using fallback RulesExporter")
        # Define a minimal fallback exporter
        class FallbackRulesExporter:
            @staticmethod
            def export_rules(*args, **kwargs):
                return "# Rules Export Failed\n\nFallback RulesExporter used."
        return FallbackRulesExporter
    return exporter

# Define public API with lazy loading
__all__ = [
    "ExportManager",
    "get_ai_exporter",
    "get_analyzer_exporter",
    "get_config_exporter",
    "get_mcp_exporter", 
    "get_summarizer_exporter",
    "get_task_manager_exporter",
    "get_rules_exporter"
]
