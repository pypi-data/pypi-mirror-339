"""Analyzer service for AMAUTA."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set
import tempfile

from amauta_ai.analyzer.complexity import ComplexityAnalyzer
from amauta_ai.analyzer.scanner import CodeScanner
from amauta_ai.analyzer.visualization import VisualizationGenerator
from amauta_ai.config.service import ConfigService
from amauta_ai.utils.logger import get_logger
from amauta_ai.ai.service import AiService

# Import the framework detection registry
from amauta_ai.analyzer.framework_detection.registry import get_registry

logger = get_logger(__name__)

class AnalyzerService:
    """
    Analyzer service for AMAUTA.

    This service is responsible for analyzing codebases and generating reports.
    """

    def __init__(
        self,
        config_service: Optional[ConfigService] = None,
        base_path: str = ".",
        use_cache: bool = True,
        cache_file: str = ".complexity_cache.json",
        use_parallel: bool = True,
        max_workers: Optional[int] = None
    ):
        """
        Initialize the analyzer service.

        Args:
            config_service: The configuration service to use. If None, a new one is created.
            base_path: The base path to analyze.
            use_cache: Whether to use cached analysis results for files that haven't changed.
            cache_file: Path to the cache file relative to base_path.
            use_parallel: Whether to use parallel processing for file analysis.
            max_workers: Maximum number of worker processes for parallel analysis.
        """
        self.config_service = config_service or ConfigService()
        self.base_path = Path(base_path).resolve()
        self.scanner = CodeScanner(config_service, base_path)
        self.complexity_analyzer = ComplexityAnalyzer(base_path)
        self.visualization_generator = VisualizationGenerator()
        self.use_cache = use_cache
        self.cache_file = cache_file
        self.use_parallel = use_parallel
        self.max_workers = max_workers
        
        # Initialize AI services lazily to avoid circular imports
        self._ai_service = None
        self._provider_selection = None
        self._prompt_manager = None
        
        # Load cache if available
        if use_cache:
            self.complexity_analyzer.load_cache(cache_file)
    
    @property
    def ai_service(self):
        """Lazily initialize the AI service."""
        if self._ai_service is None:
            from amauta_ai.ai.service import AiService
            self._ai_service = AiService(config_service=self.config_service)
        return self._ai_service
    
    @property
    def provider_selection(self):
        """Lazily initialize the provider selection service."""
        if self._provider_selection is None:
            from amauta_ai.ai.provider_selection import ProviderSelectionService
            self._provider_selection = ProviderSelectionService(self.config_service)
        return self._provider_selection
    
    @property
    def prompt_manager(self):
        """Lazily initialize the prompt manager."""
        if self._prompt_manager is None:
            from amauta_ai.ai.prompts import PromptManager
            self._prompt_manager = PromptManager()
        return self._prompt_manager

    def analyze(self, use_ai: bool = False) -> Dict[str, Any]:
        """
        Analyze the codebase and return a dictionary of results.

        Args:
            use_ai: Whether to use AI assistance for framework detection
            
        Returns:
            A dictionary containing analysis results
        """
        # Scan the directory for files
        files_by_extension = self.scanner.scan_directory()

        # Generate file summary
        file_summary = self.scanner.generate_file_summary(files_by_extension)

        # Detect package dependencies
        package_deps = self.scanner.detect_package_dependencies()

        # Collect JavaScript/TypeScript files for dependency analysis
        js_ts_files: List[Path] = []
        for ext in [".js", ".jsx", ".ts", ".tsx"]:
            if ext in files_by_extension:
                js_ts_files.extend(files_by_extension[ext])

        # Collect Python files for dependency analysis
        python_files: List[Path] = []
        if ".py" in files_by_extension:
            python_files.extend(files_by_extension[".py"])

        # Scan file dependencies
        file_dependencies: Dict[Path, Set[str]] = {}
        if js_ts_files:
            js_ts_deps = self.scanner.scan_file_dependencies(js_ts_files)
            file_dependencies.update(js_ts_deps)

        if python_files:
            python_deps = self.scanner.scan_file_dependencies(python_files)
            file_dependencies.update(python_deps)

        # Convert Path objects to strings for serialization
        str_file_dependencies: Dict[str, List[str]] = {}
        for file_path, imports in file_dependencies.items():
            rel_path = str(file_path.relative_to(self.base_path))
            str_file_dependencies[rel_path] = list(imports)

        # Analyze code complexity with caching and optional parallelization
        if self.use_parallel:
            complexity_metrics = self.complexity_analyzer.analyze_files_parallel(
                files_by_extension, 
                use_cache=self.use_cache,
                max_workers=self.max_workers
            )
        else:
            complexity_metrics = self.complexity_analyzer.analyze_files(
                files_by_extension, 
                use_cache=self.use_cache
            )
        
        # Save cache if enabled
        if self.use_cache:
            self.complexity_analyzer.save_cache(self.cache_file)

        # Get AI service if needed for framework detection
        ai_service = None
        if use_ai:
            try:
                ai_service = AiService()
            except Exception:
                # If AI service initialization fails, continue without it
                pass

        # Build the full analysis result
        result = {
            "file_summary": file_summary,
            "package_dependencies": package_deps,
            "file_dependencies": str_file_dependencies,
            "tech_stack": self._detect_tech_stack(package_deps, files_by_extension, use_ai, ai_service),
            "complexity_metrics": complexity_metrics,
        }

        return result

    def _detect_tech_stack(
        self,
        package_deps: Dict[str, Dict[str, Any]],
        files_by_extension: Dict[str, List[Path]],
        use_ai: bool = False,
        ai_service = None
    ) -> Dict[str, List[str]]:
        """
        Detect the tech stack using the framework detection system.
        
        Args:
            package_deps: Package dependency information
            files_by_extension: Files grouped by extension
            use_ai: Whether to use AI assistance for detection
            ai_service: AI service to use for detection
            
        Returns:
            A dictionary containing tech stack information
        """
        # Get the framework detector registry
        registry = get_registry()
        
        # Use the registry to detect the tech stack
        tech_stack = registry.detect_tech_stack(
            self.base_path,
            files_by_extension,
            package_deps,
            use_ai=use_ai,
            ai_service=ai_service
        )
        
        return tech_stack

    def _get_analysis_prompt(self, code: str, offline: bool = False, research: bool = False, provider: Optional[str] = None) -> str:
        """
        Get an AI-generated code analysis using provider selection.
        
        Args:
            code: The code to analyze
            offline: Whether to run in offline mode
            research: Whether to use research-optimized provider
            provider: Explicitly selected provider
            
        Returns:
            The analysis result
        """
        if offline:
            return f"Code analysis is not available in offline mode."
        
        try:
            # Import required modules here to avoid circular imports
            from amauta_ai.config.models import ProviderCapability
            from amauta_ai.ai.prompts import PromptType, PromptContext
            
            # Set required capabilities
            required_capabilities = {ProviderCapability.CODE_UNDERSTANDING}
            
            # Get provider for analysis operation
            try:
                selected_provider = self.provider_selection.get_provider_for_operation(
                    operation_type="analysis",
                    research=research,
                    provider=provider,
                    required_capabilities=required_capabilities
                )
                logger.info(f"Selected provider for code analysis: {selected_provider}")
            except Exception as e:
                logger.warning(f"Provider selection failed: {e}")
                selected_provider = provider or "anthropic"
            
            # Create prompt context
            prompt_context = PromptContext(
                provider=selected_provider,
                operation_type="analysis",
                research=research
            )
            
            # Generate code analysis prompt with appropriate template
            prompt = self.prompt_manager.generate_prompt(
                prompt_type=PromptType.CODE_ANALYSIS,
                context=prompt_context,
                template_vars={"code": code}
            )
            
            # Get system prompt
            system_prompt = self.prompt_manager.get_system_prompt(
                provider=selected_provider,
                operation_type="analysis",
                research=research
            )
            
            # Query the AI
            result = self.ai_service.query_llm(
                prompt=prompt,
                mode="analysis",
                system_prompt=system_prompt,
                provider=selected_provider,
                research=research,
                max_tokens=4000,
                temperature=0.3
            )
            
            return result
        except Exception as e:
            logger.error(f"Error generating code analysis: {e}")
            return f"Analysis could not be generated: {str(e)}"
        
    def generate_audit_md(
        self, analysis_result: Dict[str, Any], offline: bool = False, research: bool = False, provider: Optional[str] = None
    ) -> str:
        """
        Generate an audit report in Markdown format.

        Args:
            analysis_result: The analysis result
            offline: Whether to run in offline mode
            research: Whether to use research-optimized provider
            provider: Explicitly selected provider

        Returns:
            The audit report as Markdown
        """
        # Extract relevant information
        tech_stack = analysis_result.get("tech_stack", {})
        package_deps = analysis_result.get("package_dependencies", {})
        file_summary = analysis_result.get("file_summary", {})
        
        # Start building the content
        content = []
        content.append("# Project Audit Report\n\n")
        
        # Add date and project info
        from datetime import datetime
        content.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        content.append(f"Project path: {self.base_path}\n\n")
        
        # Languages section
        content.append("## Languages\n\n")
        if "languages" in tech_stack and tech_stack["languages"]:
            for lang, stats in tech_stack["languages"].items():
                content.append(f"### {lang}\n\n")
                content.append(f"- Files: {stats.get('files', 0)}\n")
                content.append(f"- Lines: {stats.get('lines', 0)}\n")
                if "extensions" in stats:
                    content.append(f"- Extensions: {', '.join(stats['extensions'])}\n")
                content.append("\n")
        else:
            content.append("No language information available.\n\n")
        
        # Frameworks section
        content.append("## Frameworks & Libraries\n\n")
        if "frameworks" in tech_stack and tech_stack["frameworks"]:
            for fw_name, fw_info in tech_stack["frameworks"].items():
                content.append(f"### {fw_name}\n\n")
                if "version" in fw_info:
                    content.append(f"- Version: {fw_info['version']}\n")
                if "usage" in fw_info:
                    content.append(f"- Usage: {fw_info['usage']}\n")
                content.append("\n")
        elif "package_managers" in tech_stack and tech_stack["package_managers"]:
            for pm_name, packages in tech_stack["package_managers"].items():
                content.append(f"### {pm_name} Packages\n\n")
                for package_name, version in packages.items():
                    content.append(f"- {package_name}: {version}\n")
                content.append("\n")
        else:
            content.append("No framework or library information available.\n\n")
        
        # Add an AI-enhanced analysis if not in offline mode
        if not offline:
            content.append("## AI Analysis\n\n")
            
            # Prepare code summary for AI analysis
            code_sample = self._extract_representative_code(analysis_result)
            if code_sample:
                analysis = self._get_analysis_prompt(
                    code_sample, 
                    offline=offline,
                    research=research,
                    provider=provider
                )
                content.append(analysis)
                content.append("\n\n")
            else:
                content.append("No code available for AI analysis.\n\n")
        
        return "".join(content)
        
    def _extract_representative_code(self, analysis_result: Dict[str, Any]) -> str:
        """Extract a representative code sample for AI analysis."""
        # Implementation to fetch a representative code sample
        # This could be from the most complex files, or main entry points
        
        # For now, return a simple representation of the project structure
        tech_stack = analysis_result.get("tech_stack", {})
        file_summary = analysis_result.get("file_summary", {})
        
        code_sample = "Project Structure:\n\n"
        
        # Add languages
        if "languages" in tech_stack:
            code_sample += "Languages:\n"
            for lang, stats in tech_stack["languages"].items():
                code_sample += f"- {lang}: {stats.get('files', 0)} files\n"
        
        # Add file types
        if file_summary:
            code_sample += "\nFile types:\n"
            for ext, count in file_summary.items():
                code_sample += f"- {ext}: {count} files\n"
        
        return code_sample

    def generate_concat_md(
        self, analysis_result: Dict[str, Any], offline: bool = False, 
        research: bool = False, provider: Optional[str] = None
    ) -> str:
        """
        Generate the concat.md file content with enhanced AI analysis.

        Args:
            analysis_result: The analysis result
            offline: Whether to run in offline mode
            research: Whether to use research-optimized provider
            provider: Explicitly selected provider

        Returns:
            The content of the concat.md file
        """
        complexity_metrics = analysis_result.get("complexity_metrics", {})
        files_metrics = complexity_metrics.get("files", {})

        # Start building the content
        content = []
        content.append("# Code Summaries\n\n")
        content.append("## Most Complex Files\n\n")

        # Identify the most complex files by cyclomatic complexity
        complex_files = []
        for file_path, metrics in files_metrics.items():
            total_complexity = 0
            for func in metrics.get("functions", []):
                total_complexity += func.get("complexity", 0)
            
            if total_complexity > 0:
                complex_files.append((file_path, total_complexity))
        
        # Sort by complexity (descending)
        complex_files.sort(key=lambda x: x[1], reverse=True)
        
        # Take the top 5 complex files
        top_complex_files = complex_files[:5]
        
        # Generate summaries for each complex file
        for file_path, complexity in top_complex_files:
            content.append(f"### {file_path}\n\n")
            content.append(f"**Complexity Score:** {complexity}\n\n")
            
            # If not in offline mode, add AI-generated insights
            if not offline:
                try:
                    # Read the file
                    full_path = self.base_path / file_path
                    if full_path.exists():
                        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                            code = f.read()
                        
                        # Generate AI insights
                        insights = self._get_code_insights(
                            code, 
                            file_path=file_path, 
                            offline=offline,
                            research=research,
                            provider=provider
                        )
                        content.append("**AI Insights:**\n\n")
                        content.append(insights)
                        content.append("\n\n")
                except Exception as e:
                    content.append(f"*Error reading file: {str(e)}*\n\n")
        
        return "".join(content)
    
    def _get_code_insights(
        self, code: str, file_path: str, offline: bool = False, 
        research: bool = False, provider: Optional[str] = None
    ) -> str:
        """
        Get AI-generated insights for a code file.
        
        Args:
            code: The code content
            file_path: The file path
            offline: Whether to run in offline mode
            research: Whether to use research-optimized provider
            provider: Explicitly selected provider
            
        Returns:
            Insights as text
        """
        if offline:
            return "*AI insights not available in offline mode*"
        
        try:
            # Import required modules here to avoid circular imports
            from amauta_ai.config.models import ProviderCapability
            from amauta_ai.ai.prompts import PromptContext
            
            # Truncate code if too long
            if len(code) > 15000:
                code = code[:15000] + "\n...(truncated)..."
            
            # Set required capabilities
            required_capabilities = {ProviderCapability.CODE_UNDERSTANDING}
            
            # Get provider for analysis operation
            try:
                selected_provider = self.provider_selection.get_provider_for_operation(
                    operation_type="analysis",
                    research=research,
                    provider=provider,
                    required_capabilities=required_capabilities
                )
                logger.info(f"Selected provider for code insights: {selected_provider}")
            except Exception as e:
                logger.warning(f"Provider selection failed: {e}")
                selected_provider = provider or "anthropic"
            
            # Create prompt context
            prompt_context = PromptContext(
                provider=selected_provider,
                operation_type="analysis",
                research=research
            )
            
            # Generate prompt
            template_vars = {
                "code": code,
                "file_path": file_path
            }
            
            prompt = f"""Analyze this code file: {file_path}
            
```
{code}
```

Provide a concise summary of what the code does and identify:
1. Key functionality
2. Any potential issues or code smells
3. Suggestions for improvement

Keep your analysis focused and insightful.
"""
            
            # Get system prompt
            system_prompt = self.prompt_manager.get_system_prompt(
                provider=selected_provider,
                operation_type="analysis",
                research=research
            )
            
            # Query the AI
            result = self.ai_service.query_llm(
                prompt=prompt,
                mode="analysis",
                system_prompt=system_prompt,
                provider=selected_provider,
                research=research,
                max_tokens=2000,
                temperature=0.3
            )
            
            return result
        except Exception as e:
            logger.error(f"Error generating code insights: {e}")
            return f"*Analysis could not be generated: {str(e)}*"

    def generate_complexity_report(
        self, analysis_result: Dict[str, Any], offline: bool = False, 
        research: bool = False, provider: Optional[str] = None
    ) -> str:
        """
        Generate the complexity.md file content with AI-enhanced explanations.

        Args:
            analysis_result: The analysis result
            offline: Whether to run in offline mode
            research: Whether to use research-optimized provider
            provider: Explicitly selected provider

        Returns:
            The content of the complexity.md file
        """
        complexity_metrics = analysis_result.get("complexity_metrics", {})
        summary = complexity_metrics.get("summary", {})
        
        content = []
        content.append("# Code Complexity Analysis\n\n")
        
        # Summary section
        content.append("## Summary\n\n")
        content.append(f"- Total Files: {summary.get('total_files', 0)}\n")
        content.append(f"- Total Functions: {summary.get('total_functions', 0)}\n")
        content.append(f"- Total Classes: {summary.get('total_classes', 0)}\n")
        content.append(f"- Total Modules: {summary.get('total_modules', 0)}\n")
        content.append(f"- Average Complexity: {summary.get('avg_complexity', 0):.2f}\n")
        content.append(f"- Maximum Complexity: {summary.get('max_complexity', 0)}\n\n")
        
        # Longest function
        longest_func = summary.get("longest_function", {})
        if longest_func:
            content.append("## Longest Function\n\n")
            content.append(f"- Name: `{longest_func.get('name', 'Unknown')}`\n")
            content.append(f"- File: {longest_func.get('file', 'Unknown')}\n")
            content.append(f"- Line Count: {longest_func.get('line_count', 0)}\n\n")
        
        # Most complex files
        files_metrics = complexity_metrics.get("files", {})
        complex_files = []
        for file_path, metrics in files_metrics.items():
            total_complexity = 0
            for func in metrics.get("functions", []):
                total_complexity += func.get("complexity", 0)
            
            if total_complexity > 0:
                complex_files.append((file_path, total_complexity))
        
        # Sort by complexity (descending)
        complex_files.sort(key=lambda x: x[1], reverse=True)
        
        # Top 10 most complex files
        content.append("## Most Complex Files\n\n")
        content.append("| File | Complexity Score |\n")
        content.append("|------|------------------|\n")
        for file_path, complexity in complex_files[:10]:
            content.append(f"| {file_path} | {complexity} |\n")
        content.append("\n")
        
        # Most complex functions
        complex_functions = []
        for file_path, metrics in files_metrics.items():
            for func in metrics.get("functions", []):
                complexity = func.get("complexity", 0)
                name = func.get("name", "Unknown")
                line_count = func.get("line_count", 0)
                
                if complexity > 0:
                    complex_functions.append((name, file_path, complexity, line_count))
        
        # Sort by complexity (descending)
        complex_functions.sort(key=lambda x: x[2], reverse=True)
        
        # Top 10 most complex functions
        content.append("## Most Complex Functions\n\n")
        content.append("| Function | File | Complexity | Line Count |\n")
        content.append("|----------|------|------------|------------|\n")
        for name, file_path, complexity, line_count in complex_functions[:10]:
            content.append(f"| `{name}` | {file_path} | {complexity} | {line_count} |\n")
        content.append("\n")
        
        # AI interpretation if not in offline mode
        if not offline and complex_files:
            content.append("## AI Complexity Interpretation\n\n")
            
            # Format complexity data for AI analysis
            complexity_data = {
                "summary": summary,
                "most_complex_files": complex_files[:5],
                "most_complex_functions": complex_functions[:5]
            }
            
            # Get AI interpretation
            interpretation = self._get_complexity_interpretation(
                complexity_data,
                offline=offline,
                research=research,
                provider=provider
            )
            
            content.append(interpretation)
            content.append("\n\n")
        
        return "".join(content)
    
    def _get_complexity_interpretation(
        self, complexity_data: Dict[str, Any], offline: bool = False,
        research: bool = False, provider: Optional[str] = None
    ) -> str:
        """
        Get AI interpretation of complexity metrics.
        
        Args:
            complexity_data: The complexity metrics data
            offline: Whether to run in offline mode
            research: Whether to use research-optimized provider
            provider: Explicitly selected provider
            
        Returns:
            Interpretation as text
        """
        if offline:
            return "*AI interpretation not available in offline mode*"
        
        try:
            # Import required modules here to avoid circular imports
            from amauta_ai.config.models import ProviderCapability
            from amauta_ai.ai.prompts import PromptContext
            
            # Set required capabilities
            required_capabilities = {ProviderCapability.CODE_UNDERSTANDING}
            
            # Get provider for analysis operation
            try:
                selected_provider = self.provider_selection.get_provider_for_operation(
                    operation_type="analysis",
                    research=research,
                    provider=provider,
                    required_capabilities=required_capabilities
                )
                logger.info(f"Selected provider for complexity interpretation: {selected_provider}")
            except Exception as e:
                logger.warning(f"Provider selection failed: {e}")
                selected_provider = provider or "anthropic"
            
            # Create prompt context
            prompt_context = PromptContext(
                provider=selected_provider,
                operation_type="analysis",
                research=research
            )
            
            # Format the data for the prompt
            summary = complexity_data["summary"]
            complex_files = complexity_data["most_complex_files"]
            complex_functions = complexity_data["most_complex_functions"]
            
            # Build the prompt
            prompt = "Interpret these code complexity metrics:\n\n"
            
            # Summary data
            prompt += "Project Summary:\n"
            prompt += f"- Total Files: {summary.get('total_files', 0)}\n"
            prompt += f"- Total Functions: {summary.get('total_functions', 0)}\n"
            prompt += f"- Average Complexity: {summary.get('avg_complexity', 0):.2f}\n"
            prompt += f"- Maximum Complexity: {summary.get('max_complexity', 0)}\n\n"
            
            # Complex files
            prompt += "Most Complex Files:\n"
            for file_path, complexity in complex_files:
                prompt += f"- {file_path}: Complexity {complexity}\n"
            prompt += "\n"
            
            # Complex functions
            prompt += "Most Complex Functions:\n"
            for name, file_path, complexity, line_count in complex_functions:
                prompt += f"- {name} in {file_path}: Complexity {complexity}, Lines {line_count}\n"
            prompt += "\n"
            
            prompt += """Based on these metrics, provide an interpretation of the codebase complexity. Include:
1. Overall assessment of complexity
2. Potential maintenance challenges
3. Specific recommendations for complex areas
4. Comparison to industry standards if possible

Keep your analysis concise and actionable."""
            
            # Get system prompt
            system_prompt = self.prompt_manager.get_system_prompt(
                provider=selected_provider,
                operation_type="analysis",
                research=research
            )
            
            # Query the AI
            result = self.ai_service.query_llm(
                prompt=prompt,
                mode="analysis",
                system_prompt=system_prompt,
                provider=selected_provider,
                research=research,
                max_tokens=2000,
                temperature=0.3
            )
            
            return result
        except Exception as e:
            logger.error(f"Error generating complexity interpretation: {e}")
            return f"*Interpretation could not be generated: {str(e)}*"

    def generate_usage_md(
        self, analysis_result: Dict[str, Any], offline: bool = False,
        research: bool = False, provider: Optional[str] = None
    ) -> str:
        """
        Generate the usage.md file content with AI-enhanced instructions.

        Args:
            analysis_result: The analysis result
            offline: Whether to run in offline mode
            research: Whether to use research-optimized provider 
            provider: Explicitly selected provider

        Returns:
            The content of the usage.md file
        """
        tech_stack = analysis_result.get("tech_stack", {})
        file_summary = analysis_result.get("file_summary", {})
        
        # Get a list of filenames
        files_metrics = analysis_result.get("complexity_metrics", {}).get("files", {})
        filenames = list(files_metrics.keys())
        
        content = []
        content.append("# Project Usage Guide\n\n")
        
        # Setup section
        content.append("## Setup\n\n")
        
        # Python setup
        if "Python" in tech_stack.get("languages", {}):
            content.append("### Python Setup\n\n")
            content.append("1. Make sure you have Python installed\n")
            
            # Check for common Python environment files
            has_requirements = "requirements.txt" in filenames
            has_pipfile = "Pipfile" in filenames
            has_poetry = "pyproject.toml" in filenames
            
            if has_requirements:
                content.append("2. Install dependencies:\n")
                content.append("   ```\n   pip install -r requirements.txt\n   ```\n")
            elif has_pipfile:
                content.append("2. Install dependencies with Pipenv:\n")
                content.append("   ```\n   pipenv install\n   ```\n")
            elif has_poetry:
                content.append("2. Install dependencies with Poetry:\n")
                content.append("   ```\n   poetry install\n   ```\n")
            else:
                content.append("2. This project might have dependencies. Check the documentation for details.\n")

        if any(
            js_lang in tech_stack.get("languages", {})
            for js_lang in ["JavaScript", "TypeScript"]
        ):
            content.append("### JavaScript/TypeScript Setup\n\n")

            if "package.json" in filenames:
                content.append("1. Make sure you have Node.js installed\n")
                content.append("2. Install dependencies:\n")
                content.append("   ```\n   npm install\n   ```\n")

                # Common npm scripts
                content.append("3. Common commands:\n")
                content.append(
                    "   ```\n   npm start    # Start the development server\n   ```\n"
                )
                content.append("   ```\n   npm test     # Run tests\n   ```\n")
                content.append(
                    "   ```\n   npm run build # Build for production\n   ```\n"
                )

        content.append("## Project Structure\n\n")
        content.append("The project is organized as follows:\n\n")
        
        # Add AI-generated usage guide if not in offline mode
        if not offline:
            try:
                # Get AI to generate more detailed usage instructions
                project_info = {
                    "tech_stack": tech_stack,
                    "file_summary": file_summary,
                    "file_count": len(filenames)
                }
                
                usage_guide = self._get_usage_guide(
                    project_info,
                    offline=offline,
                    research=research,
                    provider=provider
                )
                
                content.append("## Detailed Usage Instructions\n\n")
                content.append(usage_guide)
                content.append("\n\n")
            except Exception as e:
                logger.error(f"Error generating usage guide: {e}")
                content.append("*Error generating detailed usage instructions*\n\n")

        return "".join(content)
    
    def _get_usage_guide(
        self, project_info: Dict[str, Any], offline: bool = False,
        research: bool = False, provider: Optional[str] = None
    ) -> str:
        """
        Generate an AI-assisted usage guide.
        
        Args:
            project_info: Information about the project
            offline: Whether to run in offline mode
            research: Whether to use research-optimized provider
            provider: Explicitly selected provider
            
        Returns:
            Usage guide as text
        """
        if offline:
            return "*AI-generated usage guide not available in offline mode*"
        
        try:
            # Import required modules here to avoid circular imports
            from amauta_ai.config.models import ProviderCapability
            
            # Set required capabilities
            required_capabilities = {ProviderCapability.DOCUMENTATION}
            
            # Get provider for analysis operation
            try:
                selected_provider = self.provider_selection.get_provider_for_operation(
                    operation_type="general",
                    research=research,
                    provider=provider,
                    required_capabilities=required_capabilities
                )
                logger.info(f"Selected provider for usage guide: {selected_provider}")
            except Exception as e:
                logger.warning(f"Provider selection failed: {e}")
                selected_provider = provider or "anthropic"
            
            # Format project info for the prompt
            tech_stack_str = ""
            if "languages" in project_info["tech_stack"]:
                tech_stack_str += "Languages:\n"
                for lang, stats in project_info["tech_stack"]["languages"].items():
                    tech_stack_str += f"- {lang}: {stats.get('files', 0)} files\n"
            
            if "frameworks" in project_info["tech_stack"] and project_info["tech_stack"]["frameworks"]:
                tech_stack_str += "\nFrameworks:\n"
                for fw_name in project_info["tech_stack"]["frameworks"]:
                    tech_stack_str += f"- {fw_name}\n"
            
            # Build the prompt
            prompt = f"""Create a usage guide for a software project with the following characteristics:

{tech_stack_str}

Total files: {project_info.get('file_count', 0)}

Based on this information, provide:
1. How to run the project (common commands)
2. Typical workflow for development
3. Testing instructions if applicable
4. Deployment guidance if applicable

Keep the guide practical and focused on common operations a developer would need to perform."""
            
            # Get system prompt
            system_prompt = self.prompt_manager.get_system_prompt(
                provider=selected_provider,
                operation_type="general",
                research=research
            )
            
            # Query the AI
            result = self.ai_service.query_llm(
                prompt=prompt,
                mode="general",
                system_prompt=system_prompt,
                provider=selected_provider,
                research=research,
                max_tokens=2000,
                temperature=0.3
            )
            
            return result
        except Exception as e:
            logger.error(f"Error generating usage guide: {e}")
            return f"*Usage guide could not be generated: {str(e)}*"

    def generate_visualization_report(
        self, visualization_paths: Dict[str, str], offline: bool = False,
        research: bool = False, provider: Optional[str] = None
    ) -> str:
        """
        Generate the visualizations.md file content with AI-enhanced explanations.

        Args:
            visualization_paths: Paths to the generated visualizations
            offline: Whether to run in offline mode
            research: Whether to use research-optimized provider
            provider: Explicitly selected provider

        Returns:
            The content of the visualizations.md file
        """
        content = []
        content.append("# Project Visualizations\n\n")
        
        for viz_type, viz_path in visualization_paths.items():
            # Format the visualization type name
            viz_name = viz_type.replace("_", " ").title()
            
            content.append(f"## {viz_name}\n\n")
            
            # Add relative link to the visualization
            rel_path = Path(viz_path).name
            content.append(f"[View {viz_name}]({rel_path})\n\n")
            
            # Add AI-generated interpretation if not in offline mode
            if not offline:
                interpretation = self._get_visualization_interpretation(
                    viz_type,
                    offline=offline,
                    research=research,
                    provider=provider
                )
                content.append("### Interpretation\n\n")
                content.append(interpretation)
                content.append("\n\n")
        
        return "".join(content)
    
    def _get_visualization_interpretation(
        self, viz_type: str, offline: bool = False,
        research: bool = False, provider: Optional[str] = None
    ) -> str:
        """
        Generate an AI interpretation of a visualization.
        
        Args:
            viz_type: Type of visualization
            offline: Whether to run in offline mode
            research: Whether to use research-optimized provider
            provider: Explicitly selected provider
            
        Returns:
            Interpretation as text
        """
        if offline:
            return "*AI interpretation not available in offline mode*"
        
        try:
            # Import required modules here to avoid circular imports
            from amauta_ai.config.models import ProviderCapability
            
            # Set required capabilities
            required_capabilities = {ProviderCapability.DOCUMENTATION}
            
            # Get provider
            try:
                selected_provider = self.provider_selection.get_provider_for_operation(
                    operation_type="general",
                    research=research,
                    provider=provider,
                    required_capabilities=required_capabilities
                )
                logger.info(f"Selected provider for visualization interpretation: {selected_provider}")
            except Exception as e:
                logger.warning(f"Provider selection failed: {e}")
                selected_provider = provider or "anthropic"
            
            # Format visualization name
            viz_name = viz_type.replace("_", " ").title()
            
            # Build prompt based on visualization type
            prompt = f"Explain what information a developer can derive from a '{viz_name}' in a code analysis project. "
            
            if viz_type == "dependency_graph":
                prompt += """Focus on:
1. How to identify problematic dependencies
2. Signs of good vs. concerning architecture
3. How to use this to improve code organization
4. What patterns to look for (e.g., cycles, highly connected nodes)"""
            
            elif viz_type == "complexity_chart":
                prompt += """Focus on:
1. How to interpret complexity scores
2. What thresholds indicate potentially problematic code
3. How this information can guide refactoring priorities
4. Balancing complexity metrics with other factors"""
            
            elif viz_type == "file_type_chart":
                prompt += """Focus on:
1. What a healthy distribution of file types looks like
2. Potential red flags in file type distribution
3. How this information relates to project architecture
4. How to use this to identify areas that need documentation"""
            
            else:
                prompt += """Explain:
1. What this visualization typically shows
2. How developers can use this information
3. Key patterns to look for
4. How this contributes to codebase understanding"""
            
            # Get system prompt
            system_prompt = self.prompt_manager.get_system_prompt(
                provider=selected_provider,
                operation_type="general",
                research=research
            )
            
            # Query the AI
            result = self.ai_service.query_llm(
                prompt=prompt,
                mode="general",
                system_prompt=system_prompt,
                provider=selected_provider,
                research=research,
                max_tokens=1500,
                temperature=0.3
            )
            
            return result
        except Exception as e:
            logger.error(f"Error generating visualization interpretation: {e}")
            return f"*Interpretation could not be generated: {str(e)}*"

    def save_analysis_results(
        self, analysis_result: Dict[str, Any], output_path: Optional[str] = None
    ) -> None:
        """
        Save analysis results to a JSON file.

        Args:
            analysis_result: The analysis result
            output_path: The output path. If None, uses analysis.json in the current directory.
        """
        if output_path is None:
            output_path = "analysis.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(analysis_result, f, indent=2)

    def generate_complexity_report(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate a report of code complexity metrics.

        Args:
            analysis_result: The analysis result

        Returns:
            A Markdown formatted complexity report
        """
        if "complexity_metrics" not in analysis_result:
            return "# Complexity Analysis\n\nNo complexity metrics available."

        complexity_metrics = analysis_result["complexity_metrics"]
        summary = complexity_metrics["summary"]

        content = [
            "# Code Complexity Analysis\n\n",
            "## Summary\n\n",
            f"- **Total Functions**: {summary['total_functions']}\n",
            f"- **Total Classes**: {summary['total_classes']}\n",
            f"- **Total Modules**: {summary['total_modules']}\n",
        ]

        # Add average complexity if available
        if "avg_complexity" in summary:
            content.append(
                f"- **Average Cyclomatic Complexity**: {summary['avg_complexity']:.2f}\n"
            )

        # Add maximum complexity if available
        if "max_complexity" in summary:
            content.append(
                f"- **Maximum Cyclomatic Complexity**: {summary['max_complexity']}\n"
            )

        # Add longest function information
        if (
            "longest_function" in summary
            and summary["longest_function"]["line_count"] > 0
        ):
            longest = summary["longest_function"]
            content.append("\n## Longest Function\n\n")
            content.append(f"- **Function**: `{longest['name']}`\n")
            content.append(f"- **File**: `{longest['file']}`\n")
            content.append(f"- **Line Count**: {longest['line_count']}\n")

        # Add file details if available
        if "files" in complexity_metrics and complexity_metrics["files"]:
            content.append("\n## File Details\n\n")

            # Sort files by total function complexity
            file_complexities = []
            for file_path, file_data in complexity_metrics["files"].items():
                total_func_complexity = sum(
                    func.get("complexity", 1) for func in file_data.get("functions", [])
                )
                file_complexities.append(
                    (
                        file_path,
                        total_func_complexity,
                        len(file_data.get("functions", [])),
                    )
                )

            # Sort by total complexity
            file_complexities.sort(key=lambda x: x[1], reverse=True)

            # Create a table of file complexities
            content.append("| File | Functions | Total Complexity | Avg Complexity |\n")
            content.append("|------|-----------|------------------|---------------|\n")

            for file_path, total_complexity, func_count in file_complexities[
                :10
            ]:  # Show top 10
                avg_complexity = total_complexity / func_count if func_count > 0 else 0
                content.append(
                    f"| `{file_path}` | {func_count} | {total_complexity} | {avg_complexity:.2f} |\n"
                )

        return "".join(content)

    def generate_visualizations(
        self, analysis_result: Dict[str, Any], output_dir: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Generate visualizations from analysis results.

        Args:
            analysis_result: The analysis result
            output_dir: Directory to save visualizations. If None, uses the current directory.

        Returns:
            Dictionary mapping visualization types to file paths
        """
        viz_generator = VisualizationGenerator(output_dir=output_dir or ".")
        return viz_generator.generate_all_visualizations(analysis_result)

    def generate_visualization_report(self, visualization_paths: Dict[str, str]) -> str:
        """
        Generate a Markdown report with links to all visualizations.

        Args:
            visualization_paths: Dictionary mapping visualization types to file paths

        Returns:
            Markdown content with links to visualizations
        """
        content = [
            "# Code Analysis Visualizations\n\n",
            "The following visualizations provide insights into the codebase structure, complexity, and composition.\n\n",
        ]

        # Add links to each visualization
        if "dependency_graph" in visualization_paths:
            content.append("## [Dependency Graph](./dependency_graph.html)\n\n")
            content.append(
                "Interactive visualization of file dependencies in the codebase.\n\n"
            )

        if "complexity_chart" in visualization_paths:
            content.append("## [Code Complexity Chart](./complexity_chart.html)\n\n")
            content.append(
                "Bar chart showing the most complex files in the codebase.\n\n"
            )

        if "file_type_chart" in visualization_paths:
            content.append("## [File Type Distribution](./file_types_chart.html)\n\n")
            content.append(
                "Pie chart showing the distribution of file types in the codebase.\n\n"
            )

        content.append("## How to Use These Visualizations\n\n")
        content.append(
            "- The **Dependency Graph** allows you to explore file dependencies interactively. "
            "You can drag nodes to rearrange the graph, hover over nodes to see file paths, "
            "and zoom in/out to focus on specific areas.\n\n"
        )
        content.append(
            "- The **Code Complexity Chart** highlights files with high cyclomatic complexity. "
            "These files may be candidates for refactoring to improve maintainability.\n\n"
        )
        content.append(
            "- The **File Type Distribution** shows the composition of your codebase by file type, "
            "giving you a quick overview of the technologies used.\n\n"
        )

        return "".join(content)
