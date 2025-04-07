"""Reporter service for AMAUTA."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from amauta_ai.analyzer.service import AnalyzerService
from amauta_ai.config.service import ConfigService
from amauta_ai.task_manager.service import TaskManagerService


class ReporterService:
    """
    Reporter service for AMAUTA.

    This service is responsible for generating comprehensive project reports.
    """

    def __init__(
        self,
        config_service: Optional[ConfigService] = None,
        analyzer_service: Optional[AnalyzerService] = None,
        task_manager_service: Optional[TaskManagerService] = None,
        base_path: str = ".",
    ):
        """
        Initialize the reporter service.

        Args:
            config_service: The configuration service to use. If None, a new one is created.
            analyzer_service: The analyzer service to use. If None, a new one is created.
            task_manager_service: The task manager service to use. If None, a new one is created.
            base_path: The base path to use for generating reports.
        """
        self.config_service = config_service or ConfigService()
        self.analyzer_service = analyzer_service or AnalyzerService(
            config_service, base_path
        )
        self.task_manager_service = task_manager_service or TaskManagerService()
        self.base_path = Path(base_path).resolve()
        self.config = self.config_service.get_config()

    def generate_report(
        self,
        format: str = "md",
        analysis_result: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a comprehensive project report.

        Args:
            format: The format to generate (md, html, json)
            analysis_result: Analysis results to use. If None, a new analysis will be performed.

        Returns:
            The report content
        """
        # If no analysis result is provided, run a new analysis with error handling
        if analysis_result is None:
            try:
                # Run analyzer with timeout protection
                analysis_result = self._run_with_timeout(
                    self.analyzer_service.analyze, timeout=60
                )

                # Handle None result from analyzer
                if analysis_result is None:
                    analysis_result = self._get_fallback_analysis()
                    analysis_result["error"] = {
                        "message": "Analyzer returned None",
                        "type": "EmptyResponse",
                    }
                    logging.error("Analyzer returned None")

            except (TimeoutError, KeyboardInterrupt, ValueError, Exception) as e:
                # Use fallback minimal analysis with error information
                analysis_result = self._get_fallback_analysis()

                # Get error type and message
                error_type = type(e).__name__
                error_message = str(e)

                # Add error information
                analysis_result["error"] = {
                    "type": error_type,
                    "message": error_message,
                }

                # Log the error
                logging.error(f"Analyzer failed: {error_message}")

                # Check if the analyzer has partial results we can use
                if hasattr(self.analyzer_service, "_partial_result"):
                    partial = getattr(self.analyzer_service, "_partial_result")
                    if partial and isinstance(partial, dict):
                        # Deep merge partial results with fallback
                        analysis_result = self._merge_analysis_results(
                            analysis_result, partial
                        )

        # Get tasks
        tasks = self.task_manager_service.get_all_items()

        # Get task stats
        task_stats = self._get_task_stats(tasks)

        # Generate the report based on the format
        if format == "md":
            return self._generate_md_report(analysis_result, tasks, task_stats)
        elif format == "html":
            return self._generate_html_report(analysis_result, tasks, task_stats)
        elif format == "json":
            return self._generate_json_report(analysis_result, tasks, task_stats)
        else:
            raise ValueError(f"Unknown format: {format}")

    def _merge_analysis_results(
        self, base_result: Dict[str, Any], partial_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Deep merge partial analysis results with base result.

        Args:
            base_result: The base result to merge into
            partial_result: The partial result to merge from

        Returns:
            The merged result
        """
        result = base_result.copy()

        # Merge file summary
        if "file_summary" in partial_result:
            result["file_summary"] = {
                "total_files": partial_result["file_summary"].get("total_files", 0),
                "files_by_type": partial_result["file_summary"].get(
                    "files_by_type", {}
                ),
            }

        # Merge tech stack
        if "tech_stack" in partial_result:
            result["tech_stack"] = {
                "languages": partial_result["tech_stack"].get("languages", []),
                "frameworks": partial_result["tech_stack"].get("frameworks", []),
                "libraries": partial_result["tech_stack"].get("libraries", []),
                "tools": partial_result["tech_stack"].get("tools", []),
            }

        # Merge complexity metrics if present
        if "complexity_metrics" in partial_result:
            result["complexity_metrics"] = partial_result["complexity_metrics"]

        return result

    def _get_fallback_analysis(self) -> Dict[str, Any]:
        """
        Get a fallback minimal analysis result when analyzer fails.

        Returns:
            A dictionary with minimal structure required for report generation
        """
        return {
            "file_summary": {"total_files": 0, "files_by_type": {}},
            "tech_stack": {
                "languages": [],
                "frameworks": [],
                "libraries": [],
                "tools": [],
            },
        }

    def _run_with_timeout(self, func, timeout=60, *args, **kwargs):
        """
        Run a function with a timeout.

        Args:
            func: The function to run
            timeout: Timeout in seconds
            *args: Arguments to pass to func
            **kwargs: Keyword arguments to pass to func

        Returns:
            The result of the function

        Raises:
            TimeoutError: If the function times out
        """
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(func, *args, **kwargs)
            try:
                return future.result(timeout=timeout)
            except concurrent.futures.TimeoutError:
                # Create a custom timeout error with more context
                raise TimeoutError(
                    f"Function {func.__name__} timed out after {timeout} seconds"
                )

    def _get_task_stats(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get task statistics.

        Args:
            tasks: The tasks to analyze

        Returns:
            A dictionary containing task statistics
        """
        total_tasks = len(tasks)
        total_subtasks = sum(len(task.get("subtasks", [])) for task in tasks)

        # Count tasks by status
        status_counts = {"done": 0, "in-progress": 0, "pending": 0, "deferred": 0}

        # Count tasks by priority
        priority_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        # Count completed tasks and subtasks
        completed_tasks = 0
        completed_subtasks = 0

        for task in tasks:
            status = task.get("status", "pending")
            priority = task.get("priority", "medium")

            status_counts[status] = status_counts.get(status, 0) + 1
            priority_counts[priority] = priority_counts.get(priority, 0) + 1

            if status == "done":
                completed_tasks += 1

            for subtask in task.get("subtasks", []):
                if subtask.get("status") == "done":
                    completed_subtasks += 1

        # Calculate completion percentage
        total_items = total_tasks + total_subtasks
        completed_items = completed_tasks + completed_subtasks
        completion_percentage = (
            (completed_items / total_items * 100) if total_items > 0 else 0
        )

        return {
            "total_tasks": total_tasks,
            "total_subtasks": total_subtasks,
            "completed_tasks": completed_tasks,
            "completed_subtasks": completed_subtasks,
            "completion_percentage": round(completion_percentage),
            "status_counts": status_counts,
            "priority_counts": priority_counts,
        }

    def _format_task_for_report(
        self, task: Dict[str, Any], include_subtasks: bool = True
    ) -> str:
        """
        Format a task for the report.

        Args:
            task: The task to format
            include_subtasks: Whether to include subtask information

        Returns:
            The formatted task content
        """
        lines = []

        # Add task header
        lines.append(f"### Task {task['id']}: {task['title']}\n")

        # Add status and priority
        lines.append(f"**Status:** {task['status']}")
        lines.append(f"**Priority:** {task['priority']}\n")

        # Add description if present
        if task.get("description"):
            lines.append(f"**Description:** {task['description']}\n")

        # Add dependencies if present
        if task.get("dependencies"):
            lines.append("**Dependencies:**")
            for dep_id in task["dependencies"]:
                lines.append(f"- Task {dep_id}")
            lines.append("")

        # Add subtasks if present and requested
        if include_subtasks and task.get("subtasks"):
            lines.append("**Subtasks:**")
            for subtask in task["subtasks"]:
                status_icon = (
                    "(done)" if subtask.get("status") == "done" else "(pending)"
                )
                lines.append(f"- **{subtask['id']}:** {subtask['title']} {status_icon}")
            lines.append("")

        return "\n".join(lines)

    def _generate_md_report(
        self,
        analysis_result: Dict[str, Any],
        tasks: List[Dict[str, Any]],
        task_stats: Dict[str, Any],
    ) -> str:
        """
        Generate a Markdown report.

        Args:
            analysis_result: The analysis results
            tasks: The tasks
            task_stats: Task statistics

        Returns:
            The report content as Markdown
        """
        # Ensure required keys exist in analysis_result
        if "file_summary" not in analysis_result:
            analysis_result["file_summary"] = {"total_files": 0, "files_by_type": {}}

        if "tech_stack" not in analysis_result:
            analysis_result["tech_stack"] = {
                "languages": [],
                "frameworks": [],
                "libraries": [],
                "tools": [],
            }

        file_summary = analysis_result["file_summary"]
        tech_stack = analysis_result["tech_stack"]

        # Project information
        project_name = str(self.config.project.name) or "Project"
        project_description = (
            str(self.config.project.description) or "A software project"
        )

        # Start building the report
        md = [
            f"# {project_name} - Project Report",
            "",
            f"*Generated by AMAUTA on {datetime.now().strftime('%B %d, %Y')}*",
            "",
        ]

        # Add error information if present
        if "error" in analysis_result:
            error = analysis_result["error"]
            error_type = error.get("type", "Unknown")
            error_message = error.get("message", "Unknown error occurred")

            # Handle special cases
            if isinstance(error_type, type):
                error_type = error_type.__name__
            elif isinstance(error_type, Exception):
                error_type = error_type.__class__.__name__

            md.extend(
                [
                    "## ⚠️ Analysis Error",
                    "",
                    f"**Error Type:** {error_type}",
                    f"**Message:** {error_message}",
                    "",
                    "*Note: This report contains limited information due to analysis failure.*",
                    "",
                ]
            )

        md.extend(
            [
                "## Project Overview",
                "",
                f"{project_description}",
                "",
                "## Task Progress",
                "",
                f"**Total Tasks:** {task_stats['total_tasks']}",
                f"**Total Subtasks:** {task_stats['total_subtasks']}",
                f"**Completion:** {task_stats['completion_percentage']}%",
                "",
                "### Status Breakdown",
                "",
                f"- **Done:** {task_stats['status_counts']['done']} tasks",
                f"- **In Progress:** {task_stats['status_counts']['in-progress']} tasks",
                f"- **Pending:** {task_stats['status_counts']['pending']} tasks",
                f"- **Deferred:** {task_stats['status_counts']['deferred']} tasks",
                "",
                "### Priority Breakdown",
                "",
                f"- **Critical:** {task_stats['priority_counts']['critical']} tasks",
                f"- **High:** {task_stats['priority_counts']['high']} tasks",
                f"- **Medium:** {task_stats['priority_counts']['medium']} tasks",
                f"- **Low:** {task_stats['priority_counts']['low']} tasks",
                "",
                "## Tech Stack",
                "",
                "### Languages",
                "",
            ]
        )

        # Add tech stack details
        for language in tech_stack["languages"]:
            md.append(f"- {language}")

        md.extend(
            [
                "",
                "### Frameworks",
                "",
            ]
        )

        if tech_stack["frameworks"]:
            for framework in tech_stack["frameworks"]:
                md.append(f"- {framework}")
        else:
            md.append("- No frameworks detected")

        md.extend(
            [
                "",
                "### Libraries",
                "",
            ]
        )

        if tech_stack["libraries"]:
            for library in tech_stack["libraries"]:
                md.append(f"- {library}")
        else:
            md.append("- No significant libraries detected")

        md.extend(
            [
                "",
                "### Tools",
                "",
            ]
        )

        if tech_stack["tools"]:
            for tool in tech_stack["tools"]:
                md.append(f"- {tool}")
        else:
            md.append("- No build tools detected")

        md.extend(
            [
                "",
                "## Codebase Summary",
                "",
                f"**Total Files:** {file_summary['total_files']}",
                "",
                "### Files by Type",
                "",
            ]
        )

        for file_type, count in file_summary["files_by_type"].items():
            md.append(f"- **{file_type}:** {count} files")

        # Add task details
        md.extend(
            [
                "",
                "## Tasks",
                "",
            ]
        )

        # First, list completed tasks
        completed_tasks = [t for t in tasks if t.get("status") == "done"]
        if completed_tasks:
            md.append("### Completed Tasks")
            md.append("")
            for task in completed_tasks:
                md.append(self._format_task_for_report(task))

        # List in-progress tasks with more details
        in_progress_tasks = [t for t in tasks if t.get("status") == "in-progress"]
        if in_progress_tasks:
            md.append("### In-Progress Tasks")
            md.append("")
            for task in in_progress_tasks:
                md.append(self._format_task_for_report(task))

        # List next pending tasks with details
        pending_tasks = [t for t in tasks if t.get("status") == "pending"]
        if pending_tasks:
            md.append("### Upcoming Tasks")
            md.append("")
            # Sort by priority (critical > high > medium > low)
            priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            sorted_pending = sorted(
                pending_tasks,
                key=lambda t: priority_order.get(t.get("priority", "medium"), 2),
            )

            # Take the top 3 pending tasks
            for task in sorted_pending[:3]:
                md.append(self._format_task_for_report(task))

        return "\n".join(md)

    def _generate_html_report(
        self,
        analysis_result: Dict[str, Any],
        tasks: List[Dict[str, Any]],
        task_stats: Dict[str, Any],
    ) -> str:
        """
        Generate an HTML report.

        Args:
            analysis_result: The analysis results
            tasks: The tasks
            task_stats: Task statistics

        Returns:
            The report content as HTML
        """
        # First generate markdown
        md_content = self._generate_md_report(analysis_result, tasks, task_stats)

        # Convert markdown to HTML
        return self._md_to_html(md_content)

    def _md_to_html(self, md_content: str) -> str:
        """
        Convert markdown content to HTML.

        Args:
            md_content: The markdown content

        Returns:
            The HTML content
        """
        try:
            import markdown

            # Convert markdown to HTML
            html_body = markdown.markdown(md_content)

            # Add HTML wrapper with styling
            html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4 {{
            color: #2c3e50;
        }}
        h1 {{
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        h2 {{
            margin-top: 30px;
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }}
        pre {{
            background-color: #f8f8f8;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}
        code {{
            font-family: Consolas, monospace;
        }}
        .task-list {{
            list-style-type: none;
            padding-left: 0;
        }}
        .task-list li {{
            margin-bottom: 10px;
            padding: 10px;
            background-color: #f9f9f9;
            border-radius: 5px;
        }}
        .error-section {{
            background-color: #fff3f3;
            border-left: 4px solid #ff4444;
            padding: 15px;
            margin: 20px 0;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-box {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }}
        .stat-box h3 {{
            margin-top: 0;
            color: #2c3e50;
        }}
        .stat-box p {{
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0;
            color: #3498db;
        }}
    </style>
</head>
<body>
    <div class="content">
        {html_body}
    </div>
</body>
</html>"""

            return html

        except ImportError:
            # Fallback to basic HTML if markdown package is not available
            return f"""<!DOCTYPE html>
<html>
<body>
<pre>
{md_content}
</pre>
</body>
</html>"""

    def _generate_json_report(
        self,
        analysis_result: Dict[str, Any],
        tasks: List[Dict[str, Any]],
        task_stats: Dict[str, Any],
    ) -> str:
        """
        Generate a JSON report.

        Args:
            analysis_result: The analysis results
            tasks: The tasks
            task_stats: Task statistics

        Returns:
            The report content as JSON
        """
        # Project information
        project_name = str(self.config.project.name) or "Project"
        project_description = (
            str(self.config.project.description) or "A software project"
        )

        # Build report data
        report_data = {
            "project": {
                "name": project_name,
                "description": project_description,
                "generated_at": datetime.now().isoformat(),
            },
            "task_stats": task_stats,
            # Include file_summary and tech_stack directly at the top level for backward compatibility
            "file_summary": analysis_result.get(
                "file_summary", {"total_files": 0, "files_by_type": {}}
            ),
            "tech_stack": analysis_result.get(
                "tech_stack",
                {"languages": [], "frameworks": [], "libraries": [], "tools": []},
            ),
            "tasks": tasks,
        }

        # Add analysis as a separate field
        report_data["analysis"] = analysis_result

        # Add a status field if there was an error
        if "error" in analysis_result:
            report_data["status"] = "error"
            report_data["error"] = analysis_result["error"]
        else:
            report_data["status"] = "success"

        # Handle circular references
        try:
            # Convert to JSON
            return json.dumps(report_data, indent=2)
        except ValueError as e:
            if "Circular reference detected" in str(e):
                # Create a safe copy without circular references
                safe_report = {
                    "project": report_data["project"],
                    "task_stats": report_data["task_stats"],
                    "file_summary": report_data["file_summary"],
                    "tech_stack": report_data["tech_stack"],
                    "tasks": report_data["tasks"],
                    "status": "error",
                    "error": {
                        "message": "Circular reference detected in analysis data",
                        "type": "CircularReferenceError",
                    },
                }
                return json.dumps(safe_report, indent=2)
            else:
                raise

    def save_report(
        self, report_content: str, output_path: str, format: str = "md"
    ) -> str:
        """
        Save the report to a file.

        Args:
            report_content: The report content
            output_path: The path to save the report to
            format: The format of the report

        Returns:
            The path to the saved file
        """
        # Use the provided output path or generate one
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"project_report_{timestamp}.{format}"

        # Ensure the directory exists
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Save the report
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report_content)

        return str(output_file)

    def generate_and_save_report(
        self,
        format: str = "md",
        output_path: str = "",
    ) -> str:
        """
        Generate and save a report in one step.

        Args:
            format: The format to generate (md, html, json)
            output_path: The path to save the report to

        Returns:
            The path to the saved file
        """
        report_content = self.generate_report(format)
        return self.save_report(report_content, output_path, format)
