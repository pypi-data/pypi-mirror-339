"""
Repository summarization service for AMAUTA.

This service generates comprehensive summaries of the repository for use with AI assistants.
"""

import json
import logging
import re
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml
from rich.console import Console

console = Console()
logger = logging.getLogger(__name__)

# Configuration constants
ALLOWED_EXTENSIONS = [
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".css",
    ".html",
    ".md",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".txt",
    ".sh",
    ".bash",
    ".rs",
    ".go",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".rb",
    ".php",
    ".cs",
    ".scala",
    ".swift",
    ".gitignore",
    ".dockerignore",
    ".prettierrc",
    ".eslintrc",
    ".babelrc",
    ".editorconfig",
    ".mdc",
]
MAX_FILE_SIZE = 500 * 1024  # 500 KB
LARGE_FILE_LINE_THRESHOLD = 300  # Lines to trigger summarization


class SummarizerService:
    """Service for generating repository summaries."""

    def __init__(self, base_path: str = "."):
        """Initialize the summarizer service.

        Args:
            base_path: The base path of the repository to summarize.
        """
        self.base_path = Path(base_path).resolve()
        self.max_file_size = MAX_FILE_SIZE
        self.line_threshold = LARGE_FILE_LINE_THRESHOLD
        # Initialize repository tree structure
        self.repo_tree = {"files": []}
        # Skip directories
        self.skip_dirs = [
            "node_modules",
            "dist",
            "build",
            "coverage",
            "__pycache__",
            ".pytest_cache",
            ".venv",
            "env",
            "venv",
            ".git",
            ".github",
            ".idea",
            ".vscode",
        ]
        # Skip files
        self.skip_files = [
            "package-lock.json",
            "yarn.lock",
            "pnpm-lock.yaml",
            "concat.md",
            "concat.js",
            "amauta_summary.md",
        ]

    def generate_summary(
        self,
        output_path: str,
        include_tasks: bool = True,
        include_rules: bool = True,
        include_code: bool = True,
        max_files: int = 50,
    ) -> str:
        """Generate a comprehensive summary of the repository.

        Args:
            output_path: Path to write the summary file.
            include_tasks: Whether to include tasks from tasks.json.
            include_rules: Whether to include rules from .cursorrules.
            include_code: Whether to include core code structure.
            max_files: Maximum number of files to include when summarizing code.

        Returns:
            Path to the generated summary file.
        """
        start_time = time.time()
        output_file = Path(output_path).resolve()

        # Create the output directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Get all files to process if include_code is True
        files_to_process = []
        if include_code:
            files_to_process = self._get_all_files(max_files=max_files)

        with open(output_file, "w", encoding="utf-8") as f:
            # Write header
            f.write("# AMAUTA Repository Summary\n\n")
            f.write(
                f"*Generated with AMAUTA summarize command on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
            )

            # Write project summary
            f.write("## Project Overview\n\n")
            self._write_project_summary(f)

            # Generate repository structure
            if files_to_process:
                f.write("\n## Repository Structure\n\n")
                toc_lines = self._generate_tree_markdown(self.repo_tree)
                f.write(f"{toc_lines}\n\n---\n\n")

            # Include project configuration
            f.write("## Project Configuration\n\n")
            self._write_project_config(f)

            # Include tasks
            if include_tasks:
                f.write("\n## Tasks\n\n")
                self._write_tasks(f)

            # Include rules
            if include_rules:
                f.write("\n## Development Rules\n\n")
                self._write_rules(f)

            # Include files content
            if include_code and files_to_process:
                f.write("\n## Files\n\n")
                for file_path, rel_path in files_to_process:
                    try:
                        file_data = self._process_file(file_path, rel_path)
                        f.write(file_data)
                    except Exception as e:
                        logger.error(f"Error processing file {rel_path}: {str(e)}")
                        f.write(f"\n\n## File: `{rel_path}`\n")
                        f.write(f"- **Error:** Failed to process ({str(e)})\n\n")

        # Log summary
        end_time = time.time()
        duration = round(end_time - start_time, 2)
        logger.info(f"Summary generated in {duration} seconds")
        logger.info(f"Processed {len(files_to_process)} files")
        logger.info(f"Output written to {output_file}")

        return str(output_file)

    def _write_project_summary(self, file_handle) -> None:
        """Write a summary of the project to the summary file."""
        # Extract from README.md if available
        readme_path = self.base_path / "README.md"
        if readme_path.exists():
            readme_content = readme_path.read_text(encoding="utf-8")
            # Extract the first paragraph after the title
            lines = readme_content.split("\n")
            title_idx = -1

            for i, line in enumerate(lines):
                if line.startswith("# "):
                    title_idx = i
                    break

            if title_idx >= 0:
                # Skip empty lines after the title
                start_idx = title_idx + 1
                while start_idx < len(lines) and not lines[start_idx].strip():
                    start_idx += 1

                # Find the next empty line or the next heading
                end_idx = start_idx
                while (
                    end_idx < len(lines)
                    and lines[end_idx].strip()
                    and not lines[end_idx].startswith("#")
                ):
                    end_idx += 1

                # Extract the summary
                if start_idx < end_idx:
                    summary = "\n".join(lines[start_idx:end_idx])
                    file_handle.write(f"{summary}\n\n")

                    # If there's a Features section, include it
                    features_idx = -1
                    for i, line in enumerate(lines):
                        if line.startswith("## Features") or line.startswith(
                            "# Features"
                        ):
                            features_idx = i
                            break

                    if features_idx >= 0:
                        # Find the end of the features section
                        features_end_idx = features_idx + 1
                        while features_end_idx < len(lines) and not lines[
                            features_end_idx
                        ].startswith("##"):
                            features_end_idx += 1

                        features = "\n".join(lines[features_idx:features_end_idx])
                        file_handle.write(f"{features}\n\n")

                    return

        # Fallback: Extract from package metadata if README not found
        try:
            # Try to get info from pyproject.toml or .amautarc.yaml
            amautarc_path = self.base_path / ".amautarc.yaml"
            if amautarc_path.exists():
                with open(amautarc_path, "r", encoding="utf-8") as f:
                    config = yaml.safe_load(f)
                    if "project" in config:
                        project = config["project"]
                        file_handle.write(
                            f"**Project:** {project.get('name', 'AMAUTA')}\n\n"
                        )
                        file_handle.write(
                            f"**Description:** {project.get('description', 'AMAUTA Unified AI Development Command Center')}\n\n"
                        )
                        file_handle.write(
                            f"**Version:** {project.get('version', '0.1.0')}\n\n"
                        )
                        return

            # No project info found
            file_handle.write(
                "No project summary found. Please provide a README.md file.\n\n"
            )
        except Exception as e:
            file_handle.write(f"Error reading project metadata: {str(e)}\n\n")

    def _write_project_config(self, file_handle) -> None:
        """Write project configuration information to the summary file."""
        # Try to extract information from pyproject.toml, .amautarc.yaml, and other config files
        pyproject_path = self.base_path / "pyproject.toml"
        amautarc_path = self.base_path / ".amautarc.yaml"

        file_handle.write("### Project Files\n\n")

        if pyproject_path.exists():
            file_handle.write("#### pyproject.toml\n\n")
            file_handle.write("```toml\n")
            file_handle.write(pyproject_path.read_text(encoding="utf-8"))
            file_handle.write("\n```\n\n")

        if amautarc_path.exists():
            file_handle.write("#### .amautarc.yaml\n\n")
            file_handle.write("```yaml\n")
            file_handle.write(amautarc_path.read_text(encoding="utf-8"))
            file_handle.write("\n```\n\n")

    def _write_tasks(self, file_handle) -> None:
        """Write task information to the summary file."""
        tasks_path = self.base_path / "tasks.json"

        if not tasks_path.exists():
            file_handle.write("No tasks.json file found.\n\n")
            return

        try:
            with open(tasks_path, "r", encoding="utf-8") as tasks_file:
                tasks_data = json.load(tasks_file)

            # Format tasks
            if "tasks" in tasks_data and isinstance(tasks_data["tasks"], list):
                file_handle.write(f"Found {len(tasks_data['tasks'])} tasks.\n\n")

                for task in tasks_data["tasks"]:
                    file_handle.write(
                        f"### Task {task.get('id')}: {task.get('title')}\n\n"
                    )
                    file_handle.write(
                        f"**Status:** {task.get('status', 'Unknown')}\n\n"
                    )
                    file_handle.write(
                        f"**Priority:** {task.get('priority', 'Unknown')}\n\n"
                    )

                    if task.get("description"):
                        file_handle.write(
                            f"**Description:** {task.get('description')}\n\n"
                        )

                    if task.get("dependencies"):
                        file_handle.write(
                            f"**Dependencies:** {', '.join(task.get('dependencies'))}\n\n"
                        )

                    if task.get("details"):
                        file_handle.write("**Details:**\n\n")
                        file_handle.write(f"{task.get('details')}\n\n")

                    if task.get("test_strategy"):
                        file_handle.write("**Test Strategy:**\n\n")
                        file_handle.write(f"{task.get('test_strategy')}\n\n")

                    if task.get("subtasks") and isinstance(task.get("subtasks"), list):
                        file_handle.write("**Subtasks:**\n\n")
                        for subtask in task.get("subtasks"):
                            file_handle.write(
                                f"- **{subtask.get('id')}:** {subtask.get('title')} "
                            )
                            file_handle.write(f"({subtask.get('status', 'Unknown')})\n")
                        file_handle.write("\n")
            else:
                file_handle.write("No tasks found in tasks.json.\n\n")
        except (json.JSONDecodeError, IOError) as e:
            file_handle.write(f"Error reading tasks.json: {str(e)}\n\n")

    def _write_rules(self, file_handle) -> None:
        """Write development rules to the summary file."""
        cursorrules_path = self.base_path / ".cursorrules"
        cursor_rules_dir = self.base_path / ".cursor" / "rules"

        if cursorrules_path.exists():
            file_handle.write("### .cursorrules\n\n")
            file_handle.write("```\n")
            file_handle.write(cursorrules_path.read_text(encoding="utf-8"))
            file_handle.write("\n```\n\n")

        if cursor_rules_dir.exists() and cursor_rules_dir.is_dir():
            rule_files = list(cursor_rules_dir.glob("*.mdc"))

            for rule_file in rule_files:
                file_handle.write(f"### {rule_file.name}\n\n")
                file_handle.write("```\n")
                file_handle.write(rule_file.read_text(encoding="utf-8"))
                file_handle.write("\n```\n\n")

    def _should_skip(self, file_path: Path) -> bool:
        """Check if a file should be skipped.

        Args:
            file_path: The path to check.

        Returns:
            True if the file should be skipped, False otherwise.
        """
        # Skip output file or self
        if file_path.name in self.skip_files:
            return True

        # Skip files in specified directories
        parts = file_path.parts
        if any(part in self.skip_dirs for part in parts):
            return True

        return False

    def _is_allowed_extension(self, file_path: Path) -> bool:
        """Check if a file has an allowed extension.

        Args:
            file_path: The path to check.

        Returns:
            True if the file has an allowed extension, False otherwise.
        """
        if not ALLOWED_EXTENSIONS:
            return True
        return file_path.suffix in ALLOWED_EXTENSIONS

    def _get_all_files(self, max_files: int = 50) -> List[Tuple[Path, Path]]:
        """Get all files to process.

        Args:
            max_files: Maximum number of files to include.

        Returns:
            List of tuples (file_path, relative_path).
        """
        result = []
        processed = 0

        # First, recursively find all files
        for file_path in self.base_path.rglob("*"):
            if processed >= max_files:
                break

            if not file_path.is_file():
                continue

            if self._should_skip(file_path):
                continue

            if not self._is_allowed_extension(file_path):
                continue

            rel_path = file_path.relative_to(self.base_path)

            # Add to repository tree
            self._add_to_tree(rel_path)

            result.append((file_path, rel_path))
            processed += 1

        # Sort by file path
        result.sort(key=lambda x: str(x[1]))
        return result

    def _add_to_tree(self, rel_path: Path) -> None:
        """Add a file to the repository tree.

        Args:
            rel_path: The relative path of the file.
        """
        parts = rel_path.parts
        current = self.repo_tree

        for i, part in enumerate(parts):
            if i == len(parts) - 1:  # File
                if "files" not in current:
                    current["files"] = []
                current["files"].append(part)
            else:  # Directory
                if part not in current:
                    current[part] = {"files": []}
                current = current[part]

    def _generate_tree_markdown(self, tree: Dict, prefix: str = "") -> str:
        """Generate Markdown representation of the repository tree.

        Args:
            tree: The repository tree dictionary.
            prefix: Prefix for each line (used for recursion).

        Returns:
            Markdown representation of the tree.
        """
        lines = []

        # Process directories first
        for key in sorted(tree.keys()):
            if key == "files":
                continue

            lines.append(f"{prefix}- **{key}/**")
            subtree_lines = self._generate_tree_markdown(tree[key], prefix + "  ")
            lines.append(subtree_lines)

        # Then process files
        if "files" in tree and tree["files"]:
            for file in sorted(tree["files"]):
                lines.append(f"{prefix}- {file}")

        return "\n".join(lines)

    def _get_git_last_commit(self, file_path: Path) -> Optional[str]:
        """Get the last git commit message for a file.

        Args:
            file_path: The path to the file.

        Returns:
            The last commit message, or None if not available.
        """
        try:
            rel_path = file_path.relative_to(self.base_path)
            result = subprocess.run(
                ["git", "log", "-1", "--pretty=format:%s", "--", str(rel_path)],
                cwd=self.base_path,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout
            return None
        except Exception:
            return None

    def _summarize_content(self, content: str, ext: str) -> str:
        """Summarize file content if it's too large.

        Args:
            content: The file content.
            ext: The file extension.

        Returns:
            Summarized content if the file is large, otherwise the original content.
        """
        lines = content.split("\n")

        # If file is not too large, return as is
        if len(lines) <= self.line_threshold:
            return content

        # Summarize based on extension
        if ext in [".py", ".pyi"]:
            return self._summarize_python(content)
        elif ext in [".js", ".ts", ".jsx", ".tsx"]:
            return self._summarize_js_ts(content)
        else:
            # Generic summarization for other files
            return (
                "\n".join(lines[: self.line_threshold])
                + "\n\n... [Content truncated, showing first "
                + str(self.line_threshold)
                + " lines]"
            )

    def _summarize_python(self, content: str) -> str:
        """Summarize Python file content.

        Args:
            content: The file content.

        Returns:
            Summarized content.
        """
        lines = content.split("\n")
        imports = []
        classes = []
        functions = []

        # Extract imports, class and function definitions
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Collect imports
            if line.startswith("import ") or line.startswith("from "):
                imports.append(lines[i])

            # Collect class definitions
            elif line.startswith("class "):
                class_def = lines[i]
                if i + 1 < len(lines) and lines[i + 1].strip().startswith('"""'):
                    # Add docstring if available
                    j = i + 1
                    while j < len(lines) and not lines[j].strip().endswith('"""'):
                        j += 1
                    if j < len(lines):
                        class_def += "\n    " + "\n    ".join(lines[i + 1 : j + 1])
                        class_def += "\n    ..."
                else:
                    class_def += "\n    ..."
                classes.append(class_def)

            # Collect function definitions
            elif line.startswith("def "):
                func_def = lines[i]
                if i + 1 < len(lines) and lines[i + 1].strip().startswith('"""'):
                    # Add docstring if available
                    j = i + 1
                    while j < len(lines) and not lines[j].strip().endswith('"""'):
                        j += 1
                    if j < len(lines):
                        func_def += "\n    " + "\n    ".join(lines[i + 1 : j + 1])
                        func_def += "\n    ..."
                else:
                    func_def += "\n    ..."
                functions.append(func_def)

            i += 1

        # Construct the summary
        summary = []

        # Add file docstring if it exists
        if lines and lines[0].strip().startswith('"""'):
            j = 0
            while j < len(lines) and not lines[j].strip().endswith('"""'):
                j += 1
            if j < len(lines):
                summary.extend(lines[: j + 1])
                summary.append("")

        # Add imports
        if imports:
            summary.extend(imports)
            summary.append("")

        # Add classes
        if classes:
            summary.extend(classes)
            summary.append("")

        # Add functions
        if functions:
            summary.extend(functions)

        if not summary:
            return (
                "\n".join(lines[: self.line_threshold]) + "\n\n... [Content truncated]"
            )

        return "\n".join(summary) + "\n\n... [Structural summary of Python file]"

    def _summarize_js_ts(self, content: str) -> str:
        """Summarize JavaScript/TypeScript file content.

        Args:
            content: The file content.

        Returns:
            Summarized content.
        """
        lines = content.split("\n")
        imports = []
        exports = []
        functions = []
        classes = []

        # Extract imports, exports, functions and classes
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Collect imports
            if line.startswith("import ") or line.startswith("require("):
                imports.append(lines[i])

            # Collect exports
            elif line.startswith("export "):
                exports.append(lines[i])

            # Collect function definitions
            elif line.startswith("function ") or re.search(
                r"const\s+\w+\s*=\s*\(", line
            ):
                functions.append(lines[i] + " { ... }")

            # Collect class definitions
            elif line.startswith("class "):
                classes.append(lines[i] + " { ... }")

            i += 1

        # Construct the summary
        summary = []

        # Add imports
        if imports:
            summary.extend(imports)
            summary.append("")

        # Add exports
        if exports:
            summary.extend(exports)
            summary.append("")

        # Add classes
        if classes:
            summary.extend(classes)
            summary.append("")

        # Add functions
        if functions:
            summary.extend(functions)

        if not summary:
            return (
                "\n".join(lines[: self.line_threshold]) + "\n\n... [Content truncated]"
            )

        return "\n".join(summary) + "\n\n... [Structural summary of JS/TS file]"

    def _process_file(self, file_path: Path, rel_path: Path) -> str:
        """Process a file and return its Markdown representation.

        Args:
            file_path: The path to the file.
            rel_path: The relative path to the file.

        Returns:
            Markdown representation of the file.
        """
        file_data = ""

        # Get file metadata
        stats = file_path.stat()
        file_size = stats.st_size
        modified_date = datetime.fromtimestamp(stats.st_mtime)
        lines_count = 0

        # Read file content
        content = file_path.read_text(encoding="utf-8", errors="replace")
        lines_count = len(content.split("\n"))

        # Check if file is large
        is_large = file_size > self.max_file_size or lines_count > self.line_threshold

        # Process content
        if is_large:
            processed_content = self._summarize_content(content, file_path.suffix)
        else:
            processed_content = content

        # Get git commit info
        last_commit = self._get_git_last_commit(file_path)

        # Format file information
        file_data += f"\n\n## File: `{rel_path}`\n"
        file_data += f"- **File Size:** {file_size} bytes\n"
        file_data += f"- **Lines:** {lines_count}\n"
        file_data += (
            f"- **Last Modified:** {modified_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        )

        if last_commit:
            file_data += f"- **Last Commit:** {last_commit}\n"

        if is_large:
            file_data += "- **Note:** Content has been summarized for brevity.\n"

        # Add brief description for certain file types
        if file_path.suffix == ".py":
            file_data += self._get_python_file_description(content)

        # Add file content with appropriate syntax highlighting
        language = file_path.suffix.lstrip(".")
        if language == "py":
            language = "python"
        elif language == "ts":
            language = "typescript"
        elif language == "js":
            language = "javascript"
        elif language in ["yml", "yaml"]:
            language = "yaml"
        elif language == "md":
            language = "markdown"
        elif language == "sh":
            language = "bash"

        file_data += f"\n```{language}\n{processed_content}\n```\n"

        return file_data

    def _get_python_file_description(self, content: str) -> str:
        """Extract a brief description for a Python file.

        Args:
            content: The file content.

        Returns:
            Markdown formatted description.
        """
        lines = content.split("\n")

        # Check for module docstring
        if lines and lines[0].strip().startswith('"""'):
            # Extract the first line of the docstring
            docstring_line = lines[0].strip().strip('"""')
            if not docstring_line and len(lines) > 1:
                docstring_line = lines[1].strip()

            if docstring_line:
                return f"- **Description:** {docstring_line}\n"

        return ""


def generate_summary(
    output_path: str,
    include_tasks: bool = True,
    include_rules: bool = True,
    include_code: bool = True,
    max_files: int = 50,
    base_path: str = ".",
) -> str:
    """Generate a comprehensive summary of the repository.

    Args:
        output_path: Path to write the summary file.
        include_tasks: Whether to include tasks from tasks.json.
        include_rules: Whether to include rules from .cursorrules.
        include_code: Whether to include core code structure.
        max_files: Maximum number of files to include when summarizing code.
        base_path: The base path of the repository to summarize.

    Returns:
        Path to the generated summary file.
    """
    service = SummarizerService(base_path)
    return service.generate_summary(
        output_path=output_path,
        include_tasks=include_tasks,
        include_rules=include_rules,
        include_code=include_code,
        max_files=max_files,
    )
