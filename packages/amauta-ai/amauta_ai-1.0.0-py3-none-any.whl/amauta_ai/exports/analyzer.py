"""
Analyzer module exports for AMAUTA.

This module registers the analyzer components with the export manager.
"""

from amauta_ai.analyzer.complexity import ComplexityAnalyzer, PyAstVisitor
from amauta_ai.analyzer.scanner import CodeScanner
from amauta_ai.analyzer.service import AnalyzerService
from amauta_ai.analyzer.visualization import VisualizationGenerator
from amauta_ai.analyzer.commands.architecture import ArchitectureCommand
from amauta_ai.exports.export_manager import (
    ExportManager,
    export_class,
    export_function,
)

# Get the export manager instance
export_manager = ExportManager()

# Register classes
export_class(AnalyzerService)
export_class(CodeScanner)
export_class(ComplexityAnalyzer)
export_class(PyAstVisitor)
export_class(VisualizationGenerator)
export_class(ArchitectureCommand)

# Register methods from classes as standalone functions
# AnalyzerService methods
export_function(AnalyzerService.analyze)
export_function(AnalyzerService.generate_audit_md)
export_function(AnalyzerService.generate_complexity_report)
export_function(AnalyzerService.generate_concat_md)
export_function(AnalyzerService.generate_usage_md)
export_function(AnalyzerService.generate_visualization_report)
export_function(AnalyzerService.generate_visualizations)
export_function(AnalyzerService.save_analysis_results)

# ComplexityAnalyzer methods
export_function(ComplexityAnalyzer.analyze_files)
export_function(ComplexityAnalyzer.analyze_javascript_file)
export_function(ComplexityAnalyzer.analyze_python_file)
export_function(ComplexityAnalyzer.calculate_cyclomatic_complexity)

# CodeScanner methods
export_function(CodeScanner.detect_package_dependencies)
export_function(CodeScanner.generate_file_summary)
export_function(CodeScanner.scan_directory)
export_function(CodeScanner.scan_file_dependencies)

# VisualizationGenerator methods
export_function(VisualizationGenerator.generate_all_visualizations)
export_function(VisualizationGenerator.generate_complexity_chart)
export_function(VisualizationGenerator.generate_dependency_graph)
export_function(VisualizationGenerator.generate_file_type_chart)

# ArchitectureCommand methods
export_function(ArchitectureCommand.execute)
