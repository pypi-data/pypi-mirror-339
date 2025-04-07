"""Module for analyzing code complexity metrics."""

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple


def _add_parent_pointers(tree: ast.AST) -> None:
    """Add parent pointers to all nodes in the AST."""
    # Reverted to original implementation for testing
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node  # type: ignore [attr-defined]


# Define process_file function at module level to prevent pickling issues
def _process_file_parallel(file_path: Path, base_path: Path, cache: Dict[str, Any], 
                           cache_timestamps: Dict[str, float], use_cache: bool = True) -> Tuple[str, Dict[str, Any]]:
    """Process a single file for complexity analysis in parallel mode."""
    try:
        # Create a local complexity analyzer for this process
        analyzer = ComplexityAnalyzer(str(base_path))
        analyzer._cache = cache
        analyzer._cache_timestamps = cache_timestamps
        
        # Get relative path for reporting
        rel_path = str(file_path.relative_to(base_path))
        
        # Check cache if enabled
        if use_cache and rel_path in cache:
            file_stat = file_path.stat()
            last_modified = file_stat.st_mtime
            
            # If file timestamp matches cached timestamp, use cached result
            if cache_timestamps.get(rel_path) == last_modified:
                return rel_path, {"metrics": cache[rel_path], "cache_hit": True}
        
        # Analyze based on file extension
        ext = file_path.suffix.lower()
        
        if ext == ".py":
            metrics = analyzer.analyze_python_file(file_path)
        elif ext in (".js", ".jsx", ".ts", ".tsx"):
            metrics = analyzer.analyze_javascript_file(file_path)
        else:
            # Basic metrics for other file types
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            metrics = {
                "line_count": len(content.splitlines()),
                "character_count": len(content),
                "functions": [],
                "classes": [],
                "imports": [],
            }
        
        # Cache the result if caching is enabled
        if use_cache:
            cache[rel_path] = metrics
            file_stat = file_path.stat()
            cache_timestamps[rel_path] = file_stat.st_mtime
        
        return rel_path, {"metrics": metrics, "cache_hit": False}
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return str(file_path), {"error": str(e)}


class PyAstVisitor(ast.NodeVisitor):
    """Custom NodeVisitor to analyze Python code complexity."""

    def __init__(self) -> None:
        """Initialize the visitor."""
        self.functions: List[Dict[str, Any]] = []
        self.classes: List[Dict[str, Any]] = []
        self.imports: Set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        """Visit Import nodes."""
        for name in node.names:
            self.imports.add(name.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit ImportFrom nodes."""
        if node.module:
            self.imports.add(node.module)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """
        Visit ClassDef nodes.
        
        Optimized version that reduces redundant checks and improves performance.
        """
        # Calculate line count safely - use getattr once instead of multiple hasattr checks
        lineno = getattr(node, 'lineno', None)
        end_lineno = getattr(node, 'end_lineno', None)
        line_count = 0
        if isinstance(lineno, int) and isinstance(end_lineno, int):
            line_count = end_lineno - lineno + 1

        # Explicitly type class_info dictionary
        class_info: Dict[str, Any] = {
            "name": node.name,
            "methods": [],
            "complexity": 1,  # Base complexity
            "line_count": line_count,
        }

        # Process methods within the class - avoid creating a temporary list
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_info = self._analyze_function(item)
                class_info["methods"].append(method_info)
                # Add complexity directly
                class_info["complexity"] += method_info.get("complexity", 0)

        self.classes.append(class_info)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """
        Visit FunctionDef nodes at the module level.
        
        Optimized version that reduces redundant getattr calls and improves
        parent traversal performance.
        """
        # Get the parent node once
        parent = getattr(node, "parent", None)  # type: ignore [attr-defined]
        
        # Skip methods (functions directly in classes)
        if parent and parent.__class__.__name__ == 'ClassDef':
            self.generic_visit(node)
            return
        
        # Skip nested functions more efficiently
        curr = parent
        while curr:
            if curr.__class__.__name__ == 'FunctionDef':
                self.generic_visit(node)
                return
            curr = getattr(curr, "parent", None)  # type: ignore [attr-defined]
        
        # If we get here, it's a top-level function
        self.functions.append(self._analyze_function(node))
        self.generic_visit(node)

    def _analyze_function(self, node: ast.FunctionDef) -> Dict[str, Any]:
        """Analyze a function node and calculate its complexity."""
        # Reverted to original implementation for testing
        complexity = 1  # Base complexity

        # Calculate cyclomatic complexity
        for inner_node in ast.walk(node):
            # Control flow statements increase complexity
            if isinstance(inner_node, (ast.If, ast.While, ast.For, ast.Assert)):
                complexity += 1
            elif isinstance(inner_node, ast.BoolOp) and isinstance(
                inner_node.op, ast.And
            ):
                complexity += len(inner_node.values) - 1
            elif isinstance(inner_node, ast.BoolOp) and isinstance(
                inner_node.op, ast.Or
            ):
                complexity += len(inner_node.values) - 1
            elif isinstance(inner_node, ast.ExceptHandler):
                complexity += 1

        # Calculate line count safely
        line_count = 0
        if (
            hasattr(node, "lineno")
            and isinstance(node.lineno, int)
            and hasattr(node, "end_lineno")
            and isinstance(node.end_lineno, int)
        ):
            line_count = node.end_lineno - node.lineno + 1

        return {
            "name": node.name,
            "line_count": line_count,
            "complexity": complexity,
            "arguments": [arg.arg for arg in node.args.args],
        }

    def _get_ancestors(self, node: ast.AST) -> List[ast.AST]:
        """Get ancestor nodes using the parent field."""
        ancestors = []
        parent = getattr(node, "parent", None)  # type: ignore [attr-defined]
        while parent:
            ancestors.append(parent)
            parent = getattr(parent, "parent", None)  # type: ignore [attr-defined]
        return ancestors


class ComplexityAnalyzer:
    """
    Analyzer for code complexity metrics.

    This class is responsible for calculating various code complexity metrics
    for different programming languages.
    """

    def __init__(self, base_path: str = "."):
        """
        Initialize the complexity analyzer.

        Args:
            base_path: The base path to analyze.
        """
        self.base_path = Path(base_path).resolve()
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_timestamps: Dict[str, float] = {}

    def analyze_files(
        self, files_by_extension: Dict[str, List[Path]], use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Analyze the complexity of files.

        Args:
            files_by_extension: A dictionary mapping file extensions to lists of file paths
            use_cache: Whether to use cached results for files that haven't changed

        Returns:
            A dictionary containing complexity metrics for each file
        """
        result: Dict[str, Any] = {
            "files": {},
            "summary": {
                "total_files": sum(len(v) for v in files_by_extension.values()),
                "total_classes": 0,
                "total_modules": 0,
                "total_functions": 0,
                "avg_complexity": 0,
                "max_complexity": 0,
                "longest_function": {},
                "cache_hits": 0,  # Track cache hits
            },
        }

        total_complexity = 0
        total_functions = 0
        max_complexity = 0
        longest_function = {"name": "", "file": "", "line_count": 0}
        cache_hits = 0

        # Process Python files
        if ".py" in files_by_extension:
            for file_path in files_by_extension[".py"]:
                try:
                    # Check if we should use cached result
                    rel_path = self._get_relative_path(file_path)
                    file_mtime = file_path.stat().st_mtime
                    
                    if (use_cache and rel_path in self._cache and 
                            self._cache_timestamps.get(rel_path, 0) >= file_mtime):
                        # Use cached result
                        file_metrics = self._cache[rel_path]
                        cache_hits += 1
                    else:
                        # Analyze the file and cache the result
                        file_metrics = self.analyze_python_file(file_path)
                        self._cache[rel_path] = file_metrics
                        self._cache_timestamps[rel_path] = file_mtime
                    
                    result["files"][rel_path] = file_metrics

                    # Update summary statistics
                    functions = file_metrics.get("functions", [])
                    total_functions += len(functions)
                    result["summary"]["total_classes"] = result["summary"].get(
                        "total_classes", 0
                    ) + len(file_metrics.get("classes", []))
                    result["summary"]["total_modules"] += 1

                    # Track function complexity
                    for func in functions:
                        complexity = func.get("complexity", 0)
                        total_complexity += int(complexity)

                        # Check for max complexity
                        if complexity > max_complexity:
                            max_complexity = complexity

                        # Check for longest function
                        line_count = func.get("line_count", 0)
                        if line_count > longest_function["line_count"]:
                            longest_function = {
                                "name": func.get("name", ""),
                                "file": rel_path,
                                "line_count": line_count,
                            }
                except Exception as e:
                    print(f"Error analyzing complexity of {file_path}: {str(e)}")

        # Process JavaScript files
        for ext in [".js", ".jsx", ".ts", ".tsx"]:
            if ext in files_by_extension:
                for file_path in files_by_extension[ext]:
                    try:
                        # Check if we should use cached result
                        rel_path = self._get_relative_path(file_path)
                        file_mtime = file_path.stat().st_mtime
                        
                        if (use_cache and rel_path in self._cache and 
                                self._cache_timestamps.get(rel_path, 0) >= file_mtime):
                            # Use cached result
                            file_metrics = self._cache[rel_path]
                            cache_hits += 1
                        else:
                            # Analyze the file and cache the result
                            file_metrics = self.analyze_javascript_file(file_path)
                            self._cache[rel_path] = file_metrics
                            self._cache_timestamps[rel_path] = file_mtime
                            
                        result["files"][rel_path] = file_metrics

                        # Update summary statistics
                        functions = file_metrics.get("functions", [])
                        total_functions += len(functions)
                        result["summary"]["total_classes"] = result["summary"].get(
                            "total_classes", 0
                        ) + len(file_metrics.get("classes", []))
                        result["summary"]["total_modules"] += 1

                        # Track function complexity
                        for func in functions:
                            complexity = func.get("complexity", 0)
                            total_complexity += int(complexity)

                            # Check for max complexity
                            if complexity > max_complexity:
                                max_complexity = complexity

                            # Check for longest function
                            line_count = func.get("line_count", 0)
                            if line_count > longest_function["line_count"]:
                                longest_function = {
                                    "name": func.get("name", ""),
                                    "file": rel_path,
                                    "line_count": line_count,
                                }
                    except Exception as e:
                        print(f"Error analyzing complexity of {file_path}: {str(e)}")

        # Update final summary
        result["summary"]["total_functions"] = total_functions
        result["summary"]["max_complexity"] = max_complexity
        result["summary"]["longest_function"] = longest_function
        result["summary"]["cache_hits"] = cache_hits

        if total_functions > 0:
            result["summary"]["avg_complexity"] = total_complexity / total_functions

        return result

    def _get_relative_path(self, file_path: Path) -> str:
        """Get the relative path from the base path."""
        try:
            return str(file_path.relative_to(self.base_path))
        except ValueError:
            # If the file is not relative to the base path, return the full path
            return str(file_path)

    def analyze_python_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze the complexity of a Python file.

        Args:
            file_path: Path to the Python file

        Returns:
            A dictionary containing complexity metrics for the file
        """
        try:
            # Use context manager for proper file handling
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Calculate basic metrics once
            lines = content.splitlines()
            line_count = len(lines)
            char_count = len(content)
            
            # Pre-initialize metrics with the basic information
            metrics: Dict[str, Any] = {
                "functions": [],
                "classes": [],
                "imports": [],
                "line_count": line_count,
                "character_count": char_count,
            }

            try:
                # Parse the AST once
                tree = ast.parse(content)
                
                # Add parent pointers efficiently
                _add_parent_pointers(tree)
                
                # Set up and use the visitor
                visitor = PyAstVisitor()
                visitor.visit(tree)
                
                # Directly assign collected data
                metrics["functions"] = visitor.functions
                metrics["classes"] = visitor.classes
                metrics["imports"] = list(visitor.imports)
                
            except SyntaxError:
                # If we can't parse the file, just return basic metrics
                pass
            
            return metrics
        except Exception as e:
            # Handle other exceptions like file not found
            print(f"Error processing file {file_path}: {str(e)}")
            return {
                "functions": [],
                "classes": [],
                "imports": [],
                "line_count": 0,
                "character_count": 0,
                "error": str(e)
            }

    def analyze_javascript_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Analyze the complexity of a JavaScript/TypeScript file.

        This is a simplified implementation using regex patterns.
        For more accurate analysis, a proper JS/TS parser should be used.

        Args:
            file_path: Path to the JS/TS file

        Returns:
            A dictionary containing complexity metrics for the file
        """
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Explicitly type the metrics dictionary
        metrics: Dict[str, Any] = {
            "functions": [],
            "classes": [],
            "imports": [],
            "line_count": len(content.splitlines()),
            "character_count": len(content),
        }

        # Extract imports
        import_patterns = [
            r'import\s+(?:\* as \w+|\{\s*[\w\s,]+\}\s*|\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',  # ES6 imports
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',  # CommonJS imports
        ]

        for pattern in import_patterns:
            for match in re.finditer(pattern, content):
                if match.group(1):
                    metrics["imports"].append(match.group(1))

        # Extract function definitions
        function_patterns = [
            r"function\s+(\w+)\s*\([^)]*\)\s*\{",  # Traditional functions
            r"(?:const|let|var)\s+(\w+)\s*=\s*function\s*\([^)]*\)\s*\{",  # Function expressions
            r"(?:const|let|var)\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{",  # Arrow functions with body
            r"(?:const|let|var)\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*[^{]",  # Arrow functions without body
        ]

        for pattern in function_patterns:
            for match in re.finditer(pattern, content):
                if pattern.endswith("[^{]"):
                    # For arrow functions without body, complexity is 1
                    metrics["functions"].append(
                        {"name": match.group(1), "complexity": 1, "line_count": 1}
                    )
                else:
                    # For functions with body, need to find the closing brace
                    start_pos = match.end()
                    if "{" in content[match.start() : start_pos]:
                        # Get the function body
                        end_pos = self._find_closing_brace(content, start_pos)
                        if end_pos > start_pos:
                            body = content[start_pos:end_pos]
                            complexity = self.calculate_cyclomatic_complexity(body)

                            # Estimate line count by counting newlines
                            line_count = body.count("\n") + 1

                            metrics["functions"].append(
                                {
                                    "name": match.group(1),
                                    "complexity": complexity,
                                    "line_count": line_count,
                                }
                            )

        # Extract class definitions
        class_pattern = r"class\s+(\w+)(?:\s+extends\s+\w+)?\s*\{"
        for match in re.finditer(class_pattern, content):
            start_pos = match.end()
            end_pos = self._find_closing_brace(content, start_pos)

            if end_pos > start_pos:
                class_body = content[start_pos:end_pos]

                # Estimate class complexity by counting methods and control structures
                complexity = 1  # Base complexity
                complexity += class_body.count("function")
                complexity += class_body.count("=>")

                # Find methods in the class
                methods = []
                method_pattern = (
                    r"(?:async\s+)?(?:get|set|static\s+)?\s*(\w+)\s*\([^)]*\)\s*\{"
                )
                for method_match in re.finditer(method_pattern, class_body):
                    method_name = method_match.group(1)
                    method_start = method_match.end()
                    method_end = self._find_closing_brace(class_body, method_start)

                    if method_end > method_start:
                        method_body = class_body[method_start:method_end]
                        method_complexity = self.calculate_cyclomatic_complexity(
                            method_body
                        )

                        methods.append(
                            {
                                "name": method_name,
                                "complexity": method_complexity,
                                "line_count": method_body.count("\n") + 1,
                            }
                        )

                metrics["classes"].append(
                    {
                        "name": match.group(1),
                        "complexity": complexity,
                        "methods": methods,
                        "line_count": class_body.count("\n") + 1,
                    }
                )

        return metrics

    def _find_closing_brace(self, content: str, start_pos: int) -> int:
        """
        Find the position of the closing brace that matches the opening brace before start_pos.

        Args:
            content: Source code content
            start_pos: Position right after the opening brace

        Returns:
            Position of the matching closing brace, or -1 if not found
        """
        brace_count = 1
        pos = start_pos

        while pos < len(content):
            if content[pos] == "{":
                brace_count += 1
            elif content[pos] == "}":
                brace_count -= 1
                if brace_count == 0:
                    return pos
            pos += 1

        return -1

    def calculate_cyclomatic_complexity(self, code_snippet: str) -> int:
        """
        Calculate the cyclomatic complexity of a code snippet.

        A simplified implementation that counts control structures.

        Args:
            code_snippet: Source code snippet

        Returns:
            Estimated cyclomatic complexity
        """
        # Start with 1 (base complexity)
        complexity = 1

        # Patterns that increase complexity
        patterns = [
            r"\bif\b",  # if statements
            r"\belse if\b|\belif\b",  # else if statements
            r"\bfor\b",  # for loops
            r"\bwhile\b",  # while loops
            r"\bcase\b",  # case in switch
            r"\bcatch\b",  # catch blocks
            r"\&\&",  # logical AND
            r"\|\|",  # logical OR
            r"\?",  # ternary operator
            r"\bdo\b",  # do-while loops
            r"\bswitch\b",  # switch statements
            r"\bforeach\b",  # foreach loops (some languages)
            r"^\s*@[a-zA-Z]+ when",  # conditional annotations in some frameworks
            r"\breturn .+\s+if\s+",  # early returns with condition
            r"\bcontinue .+\s+if\s+",  # conditional continue
            r"\bbreak .+\s+if\s+",  # conditional break
        ]

        # Count occurrences of each pattern
        for pattern in patterns:
            complexity += len(re.findall(pattern, code_snippet))

        return complexity

    def clear_cache(self) -> None:
        """Clear the analysis cache."""
        self._cache.clear()
        self._cache_timestamps.clear()
        
    def save_cache(self, cache_file: str = ".complexity_cache.json") -> None:
        """
        Save the analysis cache to disk.
        
        Args:
            cache_file: Path to the cache file
        """
        import json
        
        cache_path = self.base_path / cache_file
        
        # Prepare serializable data
        cache_data = {
            "timestamps": self._cache_timestamps,
            "files": self._cache
        }
        
        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(cache_data, f)
            print(f"Cache saved to {cache_path}")
        except Exception as e:
            print(f"Error saving cache: {str(e)}")
        
    def load_cache(self, cache_file: str = ".complexity_cache.json") -> None:
        """
        Load the analysis cache from disk.
        
        Args:
            cache_file: Path to the cache file
        """
        import json
        import os
        
        cache_path = self.base_path / cache_file
        
        if not os.path.exists(cache_path):
            print(f"Cache file {cache_path} does not exist")
            return
        
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
                
            self._cache_timestamps = cache_data.get("timestamps", {})
            self._cache = cache_data.get("files", {})
            
            print(f"Loaded cache with {len(self._cache)} entries from {cache_path}")
        except Exception as e:
            print(f"Error loading cache: {str(e)}")
            # Reset cache to avoid partial data
            self.clear_cache()

    def analyze_files_parallel(
        self, files_by_extension: Dict[str, List[Path]], use_cache: bool = True, max_workers: int = None
    ) -> Dict[str, Any]:
        """
        Analyze the complexity of files in parallel.
        
        This method uses multiple processes to speed up analysis on multi-core systems.
        
        Args:
            files_by_extension: A dictionary mapping file extensions to lists of file paths
            use_cache: Whether to use cached results for files that haven't changed
            max_workers: Maximum number of worker processes (defaults to CPU count)
            
        Returns:
            A dictionary containing complexity metrics for each file
        """
        import concurrent.futures
        import os
        from functools import partial
        
        # Initialize result structure
        result: Dict[str, Any] = {
            "files": {},
            "summary": {
                "total_files": sum(len(v) for v in files_by_extension.values()),
                "total_classes": 0,
                "total_modules": 0,
                "total_functions": 0,
                "avg_complexity": 0,
                "max_complexity": 0,
                "longest_function": {},
                "cache_hits": 0,
            },
        }
        
        # Set default max_workers to CPU count
        if max_workers is None:
            max_workers = os.cpu_count() or 4
        
        # Track statistics
        total_complexity = 0
        total_functions = 0
        max_complexity = 0
        longest_function = {"name": "", "file": "", "line_count": 0}
        cache_hits = 0
        
        # Bind the process_file function with the current analyzer's state
        process_file_bound = partial(
            _process_file_parallel, 
            base_path=self.base_path,
            cache=self._cache,
            cache_timestamps=self._cache_timestamps,
            use_cache=use_cache
        )
        
        # Process files in parallel - using ThreadPoolExecutor instead of ProcessPoolExecutor
        # to avoid pickling issues with class methods
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Prepare file list
            all_files = []
            for files in files_by_extension.values():
                all_files.extend(files)
            
            # Submit all jobs
            future_to_file = {executor.submit(process_file_bound, file_path): file_path for file_path in all_files}
            
            # Collect results
            for future in concurrent.futures.as_completed(future_to_file):
                try:
                    rel_path, data = future.result()
                    
                    # Handle potential errors
                    if "error" in data:
                        print(f"Error analyzing {rel_path}: {data['error']}")
                        continue
                    
                    # Extract metrics
                    metrics = data["metrics"]
                    cache_hit = data.get("cache_hit", False)
                    
                    if cache_hit:
                        cache_hits += 1
                    
                    # Store in result
                    result["files"][rel_path] = metrics
                    
                    # Update statistics
                    functions = metrics.get("functions", [])
                    classes = metrics.get("classes", [])
                    
                    # Count functions
                    total_functions += len(functions)
                    
                    # Track complexity
                    for func in functions:
                        complexity = func.get("complexity", 0)
                        total_complexity += int(complexity)
                        
                        # Check for max complexity
                        if complexity > max_complexity:
                            max_complexity = complexity
                        
                        # Check for longest function
                        line_count = func.get("line_count", 0)
                        if line_count > longest_function["line_count"]:
                            longest_function = {
                                "name": func.get("name", ""),
                                "file": rel_path,
                                "line_count": line_count,
                            }
                    
                    # Update summary
                    result["summary"]["total_classes"] += len(classes)
                    result["summary"]["total_functions"] += len(functions)
                
                except Exception as e:
                    print(f"Error processing result: {str(e)}")
        
        # Finalize summary
        result["summary"]["cache_hits"] = cache_hits
        result["summary"]["max_complexity"] = max_complexity
        result["summary"]["longest_function"] = longest_function
        
        if total_functions > 0:
            result["summary"]["avg_complexity"] = total_complexity / total_functions
        
        return result
