"""Scanner module for code analysis."""

import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from amauta_ai.config.service import ConfigService


class CodeScanner:
    """
    Code scanner for analyzing codebases.

    This class is responsible for scanning a directory for code files,
    respecting ignore patterns and file size limits.
    """

    def __init__(
        self,
        config_service: Optional[ConfigService] = None,
        base_path: str = ".",
    ):
        """
        Initialize the code scanner.

        Args:
            config_service: The configuration service to use. If None, a new one is created.
            base_path: The base path to scan from.
        """
        self.config_service = config_service or ConfigService()
        self.base_path = Path(base_path).resolve()
        self.config = self.config_service.get_config()

        # Initialize ignored paths from config
        self.ignored_paths = set(self.config.analyzer.ignored_paths)

        # Try to load .gitignore if it exists
        self.gitignore_patterns = self._load_gitignore()

        # Get the max file size from config
        self.max_file_size_kb = self.config.analyzer.max_file_size_kb

    def _load_gitignore(self) -> List[str]:
        """
        Load the .gitignore file and parse it into patterns.

        Returns:
            A list of gitignore patterns
        """
        gitignore_path = self.base_path / ".gitignore"
        if not gitignore_path.exists():
            return []

        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Filter out comments and empty lines
            patterns = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)

            return patterns
        except Exception as e:
            print(f"Error loading .gitignore: {str(e)}")
            return []

    def _is_ignored(self, path: Path) -> bool:
        """
        Check if a path should be ignored.

        Args:
            path: The path to check

        Returns:
            True if the path should be ignored, False otherwise
        """
        # Convert to relative path from base path
        rel_path = path.relative_to(self.base_path)
        rel_path_str = str(rel_path)

        # Check direct matches in ignored_paths
        for ignored in self.ignored_paths:
            if rel_path_str == ignored or rel_path_str.startswith(f"{ignored}/"):
                return True

        # Check gitignore patterns
        for pattern in self.gitignore_patterns:
            # Simple handling of common gitignore patterns
            if pattern.endswith("/") and rel_path_str.startswith(f"{pattern}"):
                return True
            elif pattern.startswith("*") and rel_path_str.endswith(pattern[1:]):
                return True
            elif pattern == rel_path_str:
                return True

        return False

    def scan_directory(self) -> Dict[str, List[Path]]:
        """
        Scan the directory for code files.

        Returns:
            A dictionary mapping file extensions to lists of file paths
        """
        result: Dict[str, List[Path]] = {}

        for root, dirs, files in os.walk(self.base_path, topdown=True):
            # Filter out ignored directories to avoid descending into them
            dirs[:] = [d for d in dirs if not self._is_ignored(Path(root) / d)]

            for file in files:
                file_path = Path(root) / file

                # Skip ignored files
                if self._is_ignored(file_path):
                    continue

                # Skip files that are too large
                if file_path.stat().st_size > self.max_file_size_kb * 1024:
                    continue

                # Group by extension
                ext = file_path.suffix.lower()
                if ext not in result:
                    result[ext] = []

                result[ext].append(file_path)

        return result

    def scan_file_dependencies(self, files: List[Path]) -> Dict[Path, Set[str]]:
        """
        Scan files for import/require statements to detect dependencies.
        This is a simple regex-based implementation that works for common
        patterns in JS/TS/Python. For more complex analysis, a proper parser
        like Tree-sitter should be used.

        Args:
            files: List of file paths to scan

        Returns:
            A dictionary mapping file paths to sets of imported module names
        """
        result: Dict[Path, Set[str]] = {}

        for file_path in files:
            ext = file_path.suffix.lower()
            imports = set()

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                if ext in [".js", ".jsx", ".ts", ".tsx"]:
                    # Match ES6 imports
                    es6_imports = re.findall(
                        r'import\s+(?:(?:{[^}]*}|\*|\w+)\s+from\s+)?["\']([^"\']+)["\']',
                        content,
                    )
                    imports.update(es6_imports)

                    # Match require statements
                    require_imports = re.findall(
                        r'require\(["\']([^"\']+)["\']', content
                    )
                    imports.update(require_imports)

                elif ext in [".py"]:
                    # Match Python imports
                    py_imports = re.findall(r"import\s+([^\s;]+)", content)
                    imports.update(py_imports)

                    # Match Python from imports
                    from_imports = re.findall(r"from\s+([^\s;]+)\s+import", content)
                    imports.update(from_imports)

            except Exception as e:
                print(f"Error scanning {file_path}: {str(e)}")

            result[file_path] = imports

        return result

    def detect_package_dependencies(self) -> Dict[str, Dict[str, Any]]:
        """
        Detect package dependencies by analyzing package.json, requirements.txt, etc.

        Returns:
            A dictionary containing information about package dependencies
        """
        result: Dict[str, Dict[str, Any]] = {
            "node": {"dependencies": {}, "devDependencies": {}},
            "python": {"dependencies": {}, "devDependencies": {}},
            "other": {},
        }

        # Check for package.json (Node.js)
        package_json_path = self.base_path / "package.json"
        if package_json_path.exists():
            try:
                import json

                with open(package_json_path, "r", encoding="utf-8") as f:
                    package_data = json.load(f)

                # Extract dependencies
                if "dependencies" in package_data:
                    result["node"]["dependencies"] = package_data["dependencies"]

                # Extract dev dependencies
                if "devDependencies" in package_data:
                    result["node"]["devDependencies"] = package_data["devDependencies"]

            except Exception as e:
                print(f"Error parsing package.json: {str(e)}")

        # Check for requirements.txt (Python)
        requirements_path = self.base_path / "requirements.txt"
        if requirements_path.exists():
            try:
                with open(requirements_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            # Simple parsing of requirement specifiers
                            parts = re.split(r"[=><~]", line, 1)
                            package = parts[0].strip()
                            version = parts[1].strip() if len(parts) > 1 else ""
                            result["python"]["dependencies"][package] = version

            except Exception as e:
                print(f"Error parsing requirements.txt: {str(e)}")

        # Check for pyproject.toml (Python with Poetry)
        pyproject_path = self.base_path / "pyproject.toml"
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    import tomli

                    pyproject_data = tomli.loads(f.read())

                # Extract Poetry dependencies
                if "tool" in pyproject_data and "poetry" in pyproject_data["tool"]:
                    poetry_data = pyproject_data["tool"]["poetry"]

                    if "dependencies" in poetry_data:
                        # Filter out python dependency
                        deps = {
                            k: v
                            for k, v in poetry_data["dependencies"].items()
                            if k != "python"
                        }
                        result["python"]["dependencies"] = deps

                    if "dev-dependencies" in poetry_data:
                        result["python"]["devDependencies"] = poetry_data[
                            "dev-dependencies"
                        ]
                    elif "group" in poetry_data and "dev" in poetry_data["group"]:
                        if "dependencies" in poetry_data["group"]["dev"]:
                            result["python"]["devDependencies"] = poetry_data["group"][
                                "dev"
                            ]["dependencies"]

            except Exception as e:
                print(f"Error parsing pyproject.toml: {str(e)}")

        return result

    def generate_file_summary(
        self, files_by_extension: Dict[str, List[Path]]
    ) -> Dict[str, Any]:
        """
        Generate a summary of the files.

        Args:
            files_by_extension: A dictionary mapping file extensions to lists of file paths

        Returns:
            A dictionary containing file summary information
        """
        total_files = sum(len(files) for files in files_by_extension.values())
        extensions = {ext: len(files) for ext, files in files_by_extension.items()}

        # Count total lines of code
        total_code_lines = 0
        for ext, files in files_by_extension.items():
            for file_path in files:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        total_code_lines += len(f.readlines())
                except Exception:
                    # Skip files that can't be read
                    pass

        # Collect unique filenames
        filenames = set()
        for ext, files in files_by_extension.items():
            for file_path in files:
                filenames.add(file_path.name)

        return {
            "total_files": total_files,
            "extensions": extensions,
            "total_code_lines": total_code_lines,
            "filenames": list(filenames),
        }
