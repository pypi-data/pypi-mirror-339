"""
Architecture recommendation command for AMAUTA.

This module implements the 'amauta recommend-architecture' command, which analyzes
the current codebase and provides architecture recommendations.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from amauta_ai.ai.command_base import AiCommandBase
from amauta_ai.ai.prompts import PromptType, PromptContext
from amauta_ai.ai.provider_selection import ProviderMode
from amauta_ai.analyzer.service import AnalyzerService
from amauta_ai.config.models import ProviderCapability

# Configure logging
logger = logging.getLogger(__name__)

class ArchitectureCommand(AiCommandBase[Dict[str, Any]]):
    """
    Command for generating architecture recommendations.
    
    This command analyzes the current codebase and provides architecture
    recommendations using AI providers: Anthropic for codebase analysis
    and Perplexity for industry patterns research.
    """
    
    def __init__(
        self,
        path: str = ".",
        output_file: Optional[str] = None,
        offline: bool = False,
        research: bool = False,
        provider: Optional[str] = None,
        detailed: bool = False,
    ):
        """
        Initialize the architecture recommendation command.
        
        Args:
            path: Path to the project directory
            output_file: Optional file to write the output to
            offline: Whether to run in offline mode
            research: Whether to use research-optimized mode
            provider: Optional explicit provider selection
            detailed: Whether to generate more detailed recommendations
        """
        super().__init__(
            offline=offline,
            research=research,
            provider=provider,
            operation_type="analysis"
        )
        
        self.path = Path(path).resolve()
        self.output_file = output_file
        self.detailed = detailed
        
        # Create analyzer service
        self.analyzer = AnalyzerService(
            config_service=self.config_service,
            base_path=str(self.path)
        )
        
    def execute(self) -> Dict[str, Any]:
        """
        Execute the architecture recommendation command.
        
        Returns:
            Dictionary with architecture recommendations
        """
        logger.info(f"Analyzing codebase at {self.path} for architecture recommendations")
        
        # Run offline if requested
        if self.offline:
            logger.info("Running in offline mode")
            return self._generate_offline_recommendations()
        
        try:
            # Step 1: Analyze the codebase
            analysis_result = self.analyzer.analyze()
            
            # Step 2: Generate a summary of the codebase
            codebase_summary = self._generate_codebase_summary(analysis_result)
            
            # Step 3: Get architecture recommendations
            recommendations = self._get_architecture_recommendations(
                analysis_result, codebase_summary
            )
            
            # Step 4: Save recommendations if output file is specified
            if self.output_file:
                self._save_recommendations(recommendations)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error executing architecture recommendation command: {e}")
            if self.offline:
                return self._generate_offline_recommendations()
            raise
    
    def _generate_codebase_summary(self, analysis_result: Dict[str, Any]) -> str:
        """
        Generate a summary of the codebase for the AI.
        
        Args:
            analysis_result: The analysis result from AnalyzerService
            
        Returns:
            A string summarizing the codebase
        """
        tech_stack = analysis_result.get("tech_stack", {})
        file_summary = analysis_result.get("file_summary", {})
        complexity_metrics = analysis_result.get("complexity_metrics", {})
        
        # Build a structured summary
        summary = []
        
        # Project overview
        summary.append("Project Overview:")
        total_files = sum(count for ext, count in file_summary.items())
        summary.append(f"- Total files: {total_files}")
        
        # Languages
        if "languages" in tech_stack:
            summary.append("\nLanguages:")
            for lang, stats in tech_stack.get("languages", {}).items():
                files = stats.get("files", 0)
                lines = stats.get("lines", 0)
                summary.append(f"- {lang}: {files} files, {lines} lines")
        
        # Main directories and structure
        summary.append("\nMain Directories:")
        try:
            # Get top-level directories and their file counts
            top_dirs = {}
            for file_path in analysis_result.get("file_dependencies", {}).keys():
                path = Path(file_path)
                top_dir = path.parts[0] if path.parts else ""
                if top_dir:
                    top_dirs[top_dir] = top_dirs.get(top_dir, 0) + 1
            
            # Add directories to summary
            for dir_name, count in sorted(top_dirs.items(), key=lambda x: x[1], reverse=True)[:10]:
                summary.append(f"- {dir_name}/: {count} files")
        except Exception as e:
            logger.warning(f"Error analyzing directory structure: {e}")
        
        # Complexity overview
        if complexity_metrics:
            summary.append("\nComplexity Overview:")
            complexity_summary = complexity_metrics.get("summary", {})
            summary.append(f"- Total functions: {complexity_summary.get('total_functions', 0)}")
            summary.append(f"- Average complexity: {complexity_summary.get('avg_complexity', 0):.2f}")
            summary.append(f"- Maximum complexity: {complexity_summary.get('max_complexity', 0)}")
        
        # Dependencies
        if "file_dependencies" in analysis_result:
            summary.append("\nDependencies:")
            dep_count = len(analysis_result.get("file_dependencies", {}))
            summary.append(f"- {dep_count} files with dependencies mapped")
            
            # Get packages if available
            if "package_dependencies" in analysis_result:
                pkg_deps = analysis_result.get("package_dependencies", {})
                for pkg_type, deps in pkg_deps.items():
                    if deps.get("dependencies"):
                        summary.append(f"- {pkg_type.capitalize()} dependencies: {len(deps.get('dependencies', {}))} packages")
        
        return "\n".join(summary)
    
    def _get_architecture_recommendations(
        self, analysis_result: Dict[str, Any], codebase_summary: str
    ) -> Dict[str, Any]:
        """
        Generate architecture recommendations using AI.
        
        Args:
            analysis_result: The analysis result from AnalyzerService
            codebase_summary: A summary of the codebase
            
        Returns:
            Dictionary with architecture recommendations
        """
        # Get tech stack from analysis
        tech_stack = analysis_result.get("tech_stack", {})
        
        # Step 1: Select provider for code structure analysis
        codebase_provider = self._select_provider_for_codebase_analysis()
        logger.info(f"Selected provider for codebase analysis: {codebase_provider}")
        
        # Step 2: Select provider for industry patterns (if research mode)
        patterns_provider = None
        if self.research:
            patterns_provider = self._select_provider_for_patterns_research()
            logger.info(f"Selected provider for industry patterns: {patterns_provider}")
        
        # Step 3: Generate codebase architecture analysis
        codebase_analysis = self._analyze_codebase_architecture(
            codebase_provider, codebase_summary, tech_stack
        )
        
        # Step 4: If research mode, generate industry patterns analysis
        industry_patterns = None
        if self.research and patterns_provider and patterns_provider != codebase_provider:
            industry_patterns = self._analyze_industry_patterns(
                patterns_provider, codebase_summary, tech_stack
            )
        
        # Step 5: Combine the analyses into recommendations
        recommendations = {
            "codebase_analysis": codebase_analysis,
            "industry_patterns": industry_patterns,
            "recommendations": self._generate_combined_recommendations(
                codebase_analysis, industry_patterns, tech_stack
            ),
            "tech_stack": tech_stack
        }
        
        return recommendations
    
    def _select_provider_for_codebase_analysis(self) -> str:
        """
        Select the best provider for codebase architecture analysis.
        
        Anthropic is preferred for codebase analysis due to its strong
        code understanding capabilities.
        
        Returns:
            Selected provider name
        """
        # Require code understanding capability
        required_capabilities = {ProviderCapability.CODE_UNDERSTANDING}
        
        try:
            # Select provider (prefer Anthropic for code analysis)
            provider = self.select_provider(
                mode=ProviderMode.ANALYSIS,
                required_capabilities=required_capabilities
            )
            # If an explicit provider was set by the user, use that
            if self.provider:
                return provider
            
            # Otherwise prefer Anthropic for code understanding
            available_providers = self.provider_selection_service.get_available_providers()
            if "anthropic" in available_providers:
                return "anthropic"
            
            return provider
        except Exception as e:
            logger.warning(f"Error selecting provider for codebase analysis: {e}")
            return "anthropic"  # Default to Anthropic
    
    def _select_provider_for_patterns_research(self) -> str:
        """
        Select the best provider for researching industry patterns.
        
        Perplexity is preferred for industry patterns research due to
        its strong research and up-to-date knowledge capabilities.
        
        Returns:
            Selected provider name
        """
        # Require research capability
        required_capabilities = {ProviderCapability.RESEARCH}
        
        try:
            # Select provider (prefer Perplexity for research)
            provider = self.select_provider(
                mode=ProviderMode.RESEARCH,
                required_capabilities=required_capabilities
            )
            # If an explicit provider was set by the user, use that
            if self.provider:
                return provider
            
            # Otherwise prefer Perplexity for research
            available_providers = self.provider_selection_service.get_available_providers()
            if "perplexity" in available_providers:
                return "perplexity"
            
            return provider
        except Exception as e:
            logger.warning(f"Error selecting provider for patterns research: {e}")
            return "perplexity"  # Default to Perplexity
    
    def _analyze_codebase_architecture(
        self, provider: str, codebase_summary: str, tech_stack: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze the codebase architecture using the selected provider.
        
        Args:
            provider: The AI provider to use
            codebase_summary: Summary of the codebase
            tech_stack: Tech stack information
            
        Returns:
            Dictionary with architecture analysis
        """
        logger.info(f"Analyzing codebase architecture with {provider}")
        
        try:
            # Create context for the prompt
            context = PromptContext(
                provider=provider,
                operation_type="analysis",
                research=self.research
            )
            
            # Generate the prompt
            prompt = self.prompt_manager.generate_prompt(
                prompt_type=PromptType.ARCHITECTURE_RECOMMENDATION,
                context=context,
                template_vars={
                    "codebase_summary": codebase_summary
                }
            )
            
            # Get system prompt
            system_prompt = self.prompt_manager.get_system_prompt(
                provider=provider,
                operation_type="analysis",
                research=self.research
            )
            
            # Query the AI
            result = self.ai_service.query_llm(
                prompt=prompt,
                system_prompt=system_prompt,
                provider=provider,
                research=self.research,
                mode="analysis",
                max_tokens=4000,
                temperature=0.2
            )
            
            return {
                "provider": provider,
                "analysis": result
            }
        except Exception as e:
            logger.error(f"Error analyzing codebase architecture: {e}")
            return {
                "provider": provider,
                "analysis": f"Error analyzing codebase architecture: {str(e)}",
                "error": True
            }
    
    def _analyze_industry_patterns(
        self, provider: str, codebase_summary: str, tech_stack: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Research industry patterns using the selected provider.
        
        Args:
            provider: The AI provider to use
            codebase_summary: Summary of the codebase
            tech_stack: Tech stack information
            
        Returns:
            Dictionary with industry patterns analysis
        """
        logger.info(f"Researching industry patterns with {provider}")
        
        try:
            # Create context for the prompt with analyze_existing flag
            context = PromptContext(
                provider=provider,
                operation_type="research",
                research=True  # Always use research mode for patterns
            )
            
            # Extract technologies to focus research
            languages = list(tech_stack.get("languages", {}).keys())
            frameworks = list(tech_stack.get("frameworks", {}).keys())
            tech_focus = ", ".join(languages + frameworks)
            
            # Generate a research-focused prompt
            prompt = f"""Research modern architecture patterns and best practices for codebases similar to this:

{codebase_summary}

Focus on architectural patterns and best practices for {tech_focus}.

Include:
1. Modern architecture patterns appropriate for this tech stack
2. Industry best practices for code organization and structure
3. References to authoritative sources, tutorials, or case studies
4. Specific recommendations that could improve this codebase

Your response should be research-backed and include citations where possible."""
            
            # Get system prompt
            system_prompt = self.prompt_manager.get_system_prompt(
                provider=provider,
                operation_type="research",
                research=True
            )
            
            # Query the AI
            result = self.ai_service.query_llm(
                prompt=prompt,
                system_prompt=system_prompt,
                provider=provider,
                research=True,
                mode="research",
                max_tokens=4000,
                temperature=0.3
            )
            
            return {
                "provider": provider,
                "analysis": result
            }
        except Exception as e:
            logger.error(f"Error researching industry patterns: {e}")
            return {
                "provider": provider,
                "analysis": f"Error researching industry patterns: {str(e)}",
                "error": True
            }
    
    def _generate_combined_recommendations(
        self, 
        codebase_analysis: Dict[str, Any], 
        industry_patterns: Optional[Dict[str, Any]],
        tech_stack: Dict[str, Any]
    ) -> str:
        """
        Generate combined recommendations from codebase analysis and industry patterns.
        
        Args:
            codebase_analysis: The codebase architecture analysis
            industry_patterns: The industry patterns analysis (optional)
            tech_stack: Tech stack information
            
        Returns:
            Combined recommendations text
        """
        # If we only have codebase analysis, return it
        if not industry_patterns:
            return codebase_analysis.get("analysis", "")
        
        # If we have both analyses, combine them
        try:
            # Select a provider for generating the combined recommendations
            # (prefer the one that is not in error state)
            provider = codebase_analysis.get("provider", "anthropic")
            if codebase_analysis.get("error") and not industry_patterns.get("error"):
                provider = industry_patterns.get("provider", "perplexity")
            
            # Generate combined recommendations prompt
            prompt = f"""Synthesize these two architectural analyses into a cohesive set of recommendations:

CODEBASE ANALYSIS:
{codebase_analysis.get("analysis", "")}

INDUSTRY PATTERNS AND BEST PRACTICES:
{industry_patterns.get("analysis", "")}

Create a unified set of architectural recommendations that combines the codebase-specific insights with industry best practices.
Focus on practical, actionable recommendations that would improve the architecture.
Organize your response into clear sections with specific, prioritized recommendations."""
            
            # Get system prompt
            system_prompt = self.prompt_manager.get_system_prompt(
                provider=provider,
                operation_type="analysis",
                research=self.research
            )
            
            # Query the AI
            result = self.ai_service.query_llm(
                prompt=prompt,
                system_prompt=system_prompt,
                provider=provider,
                research=self.research,
                mode="analysis",
                max_tokens=4000,
                temperature=0.2
            )
            
            return result
        except Exception as e:
            logger.error(f"Error generating combined recommendations: {e}")
            # Fall back to concatenating the analyses
            combined = []
            combined.append("# Architecture Recommendations\n")
            combined.append("## Codebase Analysis\n")
            combined.append(codebase_analysis.get("analysis", ""))
            combined.append("\n\n## Industry Patterns and Best Practices\n")
            combined.append(industry_patterns.get("analysis", ""))
            return "\n".join(combined)
    
    def _save_recommendations(self, recommendations: Dict[str, Any]) -> None:
        """
        Save the recommendations to a file.
        
        Args:
            recommendations: The recommendations to save
        """
        if not self.output_file:
            return
        
        try:
            # Get output path
            output_path = Path(self.output_file)
            
            # Determine format based on extension
            if output_path.suffix.lower() == '.json':
                # Save as JSON
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(recommendations, f, indent=2)
            else:
                # Save as Markdown
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write("# Architecture Recommendations\n\n")
                    
                    # Write main recommendations
                    f.write(recommendations.get("recommendations", ""))
                    
                    # Write additional sections if detailed mode
                    if self.detailed:
                        if "codebase_analysis" in recommendations:
                            f.write("\n\n## Codebase Analysis\n\n")
                            f.write(recommendations["codebase_analysis"].get("analysis", ""))
                        
                        if "industry_patterns" in recommendations and recommendations["industry_patterns"]:
                            f.write("\n\n## Industry Patterns Research\n\n")
                            f.write(recommendations["industry_patterns"].get("analysis", ""))
            
            logger.info(f"Recommendations saved to {output_path}")
        except Exception as e:
            logger.error(f"Error saving recommendations: {e}")
            raise
    
    def _generate_offline_recommendations(self) -> Dict[str, Any]:
        """
        Generate offline recommendations.
        
        Returns:
            Dictionary with offline recommendations
        """
        return {
            "codebase_analysis": {
                "provider": "offline",
                "analysis": "Offline mode: Architecture analysis requires AI provider access. "
                           "Please ensure API keys are configured in your .env file and run "
                           "without the --offline flag."
            },
            "industry_patterns": None,
            "recommendations": "Offline mode: Architecture recommendations require AI provider access."
        } 