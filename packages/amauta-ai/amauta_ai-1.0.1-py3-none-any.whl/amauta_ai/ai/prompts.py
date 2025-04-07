"""
Prompt management for AI providers.

This module provides specialized prompting strategies for different AI providers,
allowing AMAUTA to tailor prompts to each provider's strengths and requirements.
"""

import logging
from enum import Enum
from typing import Dict, Optional, Any, Union, List

from amauta_ai.config.models import ProviderCapability

# Configure logging
logger = logging.getLogger(__name__)

class PromptType(str, Enum):
    """Types of prompts by function."""
    TASK_CREATION = "task_creation"
    TASK_EXPANSION = "task_expansion"
    CODE_ANALYSIS = "code_analysis"
    PRD_PARSING = "prd_parsing"
    COMPLEXITY_ANALYSIS = "complexity_analysis"
    RESEARCH = "research"
    ARCHITECTURE_RECOMMENDATION = "architecture_recommendation"
    CODE_GENERATION = "code_generation"

class PromptContext:
    """
    Context for dynamic prompt generation.
    
    This class holds contextual information for prompt generation,
    which can be used to tailor prompts to specific situations.
    """
    
    def __init__(self, 
                 provider: str, 
                 operation_type: str,
                 research: bool = False,
                 **kwargs: Any) -> None:
        """
        Initialize prompt context.
        
        Args:
            provider: The AI provider to use
            operation_type: The type of operation
            research: Whether research mode is enabled
            **kwargs: Additional context parameters
        """
        self.provider = provider
        self.operation_type = operation_type
        self.research = research
        self.context_data = kwargs
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get a context value by key."""
        return self.context_data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a context value."""
        self.context_data[key] = value

class PromptManager:
    """
    Manager for generating provider-optimized prompts.
    
    This class centralizes prompt generation, providing a unified interface
    for generating prompts tailored to specific providers and operations.
    """
    
    def __init__(self) -> None:
        """Initialize the prompt manager."""
        self.templates = PromptTemplates()
        
    def generate_prompt(self, 
                         prompt_type: Union[PromptType, str],
                         context: PromptContext,
                         template_vars: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a provider-optimized prompt.
        
        Args:
            prompt_type: The type of prompt to generate
            context: Context for prompt generation
            template_vars: Variables to use in the template
            
        Returns:
            The generated prompt
        """
        if isinstance(prompt_type, str):
            try:
                prompt_type = PromptType(prompt_type)
            except ValueError:
                logger.warning(f"Unknown prompt type: {prompt_type}, using default template")
                # We'll continue with the string version and let the template methods handle it
        
        # Get the template method based on prompt type
        template_method = self._get_template_method(prompt_type)
        
        # Generate the template
        template = template_method(
            provider=context.provider,
            research=context.research,
            **(context.context_data or {})
        )
        
        # Apply template variables
        if template_vars:
            return self._apply_template_vars(template, template_vars)
        
        return template
    
    def _get_template_method(self, prompt_type: Union[PromptType, str]):
        """Get the template method for a prompt type."""
        type_str = prompt_type.value if isinstance(prompt_type, PromptType) else prompt_type
        
        method_map = {
            PromptType.TASK_CREATION.value: self.templates.get_task_creation_prompt,
            PromptType.TASK_EXPANSION.value: self.templates.get_task_expansion_prompt,
            PromptType.CODE_ANALYSIS.value: self.templates.get_code_analysis_prompt,
            PromptType.PRD_PARSING.value: self.templates.get_prd_parsing_prompt,
            PromptType.COMPLEXITY_ANALYSIS.value: self.templates.get_complexity_analysis_prompt,
            PromptType.RESEARCH.value: self.templates.get_research_prompt,
            PromptType.ARCHITECTURE_RECOMMENDATION.value: self.templates.get_architecture_recommendation_prompt,
            PromptType.CODE_GENERATION.value: self.templates.get_code_generation_prompt,
        }
        
        return method_map.get(type_str, self.templates.get_default_prompt)
    
    def _apply_template_vars(self, template: str, vars_dict: Dict[str, Any]) -> str:
        """Apply template variables to a template string."""
        result = template
        for key, value in vars_dict.items():
            placeholder = f"{{{{{key}}}}}"
            result = result.replace(placeholder, str(value))
        return result

    def get_system_prompt(self, provider: str, operation_type: str, research: bool = False) -> str:
        """
        Get a provider-specific system prompt.
        
        Args:
            provider: The AI provider to use
            operation_type: The type of operation
            research: Whether research mode is enabled
            
        Returns:
            A system prompt optimized for the provider and operation
        """
        if provider == "anthropic":
            return self._get_anthropic_system_prompt(operation_type, research)
        elif provider == "perplexity":
            return self._get_perplexity_system_prompt(operation_type, research)
        else:
            return self._get_default_system_prompt(operation_type, research)
    
    def _get_anthropic_system_prompt(self, operation_type: str, research: bool) -> str:
        """Get a system prompt for Anthropic."""
        base_prompt = "You are Claude, an advanced AI assistant created by Anthropic."
        
        if research:
            base_prompt += " You're operating in research mode, providing comprehensive, well-researched information with citations where possible."
        
        if operation_type == "code":
            base_prompt += " You excel at code analysis, generation, and review. Explain your reasoning clearly when discussing code."
        elif operation_type == "task":
            base_prompt += " You're helping to define, organize, and break down tasks effectively."
        elif operation_type == "analysis":
            base_prompt += " You're helping with detailed analysis of projects, code, and requirements."
        
        return base_prompt
    
    def _get_perplexity_system_prompt(self, operation_type: str, research: bool) -> str:
        """Get a system prompt for Perplexity."""
        base_prompt = "You are an AI assistant powered by Perplexity."
        
        if research:
            base_prompt += " You have access to up-to-date information and can provide well-researched responses with citations."
        
        if operation_type == "code":
            base_prompt += " Focus on providing accurate, idiomatic code examples with clear explanations."
        elif operation_type == "task":
            base_prompt += " Help organize and structure tasks efficiently with industry best practices in mind."
        elif operation_type == "analysis":
            base_prompt += " Provide thorough analysis with reference to industry standards and best practices."
        
        return base_prompt
    
    def _get_default_system_prompt(self, operation_type: str, research: bool) -> str:
        """Get a default system prompt."""
        base_prompt = "You are an AI assistant helping with software development tasks."
        
        if research:
            base_prompt += " Provide well-researched information with citations where possible."
        
        if operation_type == "code":
            base_prompt += " Focus on clear, maintainable code examples."
        elif operation_type == "task":
            base_prompt += " Help organize and structure tasks effectively."
        elif operation_type == "analysis":
            base_prompt += " Provide detailed analysis and recommendations."
        
        return base_prompt

class PromptTemplates:
    """
    Prompt templates tailored for different AI providers and functions.
    
    This class provides prompt templates optimized for each provider's strengths
    and response style. Each method returns the appropriate template based on
    the provider and whether research mode is enabled.
    """
    
    def get_default_prompt(self, provider: str, research: bool = False, **kwargs: Any) -> str:
        """
        Get a default prompt template.
        
        Args:
            provider: The AI provider to use
            research: Whether to use research mode
            
        Returns:
            The prompt template
        """
        return """
        Please provide a detailed response to the following:
        
        {{input}}
        """
    
    def get_task_creation_prompt(self, provider: str, research: bool = False, **kwargs: Any) -> str:
        """
        Get a prompt template for task creation.
        
        Args:
            provider: The AI provider to use
            research: Whether to use research mode
            
        Returns:
            The prompt template
        """
        if provider == "anthropic":
            # Anthropic excels at following detailed instructions and structure
            return """
            Create a well-defined task based on the following description.
            
            Description: {{description}}
            
            Your response should be in JSON format with the following structure:
            {
              "title": "A clear, concise title for the task",
              "description": "A detailed description of what needs to be done",
              "details": "Technical details, implementation notes, and any specific requirements",
              "test_strategy": "How to verify the task is completed correctly"
            }
            
            Make the title brief but descriptive, and provide a comprehensive description.
            The details section should include technical considerations and implementation guidance.
            """
        elif provider == "perplexity" and research:
            # Perplexity in research mode can provide industry context
            return """
            Create a well-defined task based on the following description, with industry best practices and references.
            
            Description: {{description}}
            
            Your response should include:
            1. A clear, concise title
            2. A detailed description with industry context
            3. Technical details and implementation guidance with references to current best practices
            4. Recommendations for testing and validation
            
            Format your response as a JSON object with title, description, details, and test_strategy fields.
            Include specific library recommendations, architectural patterns, or techniques where appropriate,
            citing industry sources or documentation.
            """
        else:
            # Default template
            return """
            Create a task based on the following description:
            {{description}}
            
            Format your response as a JSON object with title, description, details, and test_strategy fields.
            """
    
    def get_task_expansion_prompt(self, provider: str, research: bool = False, complexity_data: Optional[Dict] = None, **kwargs: Any) -> str:
        """
        Get a prompt template for task expansion.
        
        Args:
            provider: The AI provider to use
            research: Whether to use research mode
            complexity_data: Optional complexity analysis data to guide expansion
            
        Returns:
            The prompt template
        """
        if provider == "anthropic":
            # Use named placeholders for the template
            base_template = """
            Expand the following task into a set of well-defined subtasks.
            
            Task: {{task}}
            
            {0}
            
            Your response should be a JSON array of subtasks, each with:
            {{
              "title": "Clear, concise subtask title",
              "description": "Detailed description of what needs to be done",
              "dependencies": ["ids of tasks this depends on"],
              "estimated_hours": estimated hours as a number
            }}
            
            Ensure the subtasks:
            1. Are logically ordered
            2. Have clear dependencies
            3. Are sized appropriately (2-8 hours each)
            4. Cover all aspects of the parent task
            """
            
            if complexity_data:
                complexity_guidance = f"""
                Complexity Analysis:
                - Overall Complexity: {complexity_data.get('complexity', 'medium')}
                - Recommended Subtasks: {complexity_data.get('recommendedSubtasks', 3)}
                - Risk Factors: {', '.join(complexity_data.get('riskFactors', []))}
                """
            else:
                complexity_guidance = ""
                
            return base_template.format(complexity_guidance)
            
        elif provider == "perplexity" and research:
            return """
            Expand the following task into subtasks, incorporating industry best practices and current technical standards.
            
            Task: {{task}}
            
            For each subtask, provide:
            1. A clear title
            2. A detailed description with implementation guidance
            3. Dependencies on other subtasks
            4. Time estimation
            5. Technical considerations and recommended approaches
            6. References to relevant documentation or examples
            
            Format your response as a JSON array of subtask objects.
            """
        else:
            return """
            Break down the following task into subtasks:
            {{task}}
            
            Format your response as a JSON array of subtask objects with title, description, dependencies, and estimated_hours fields.
            """
    
    def get_complexity_analysis_prompt(self, provider: str, research: bool = False, **kwargs: Any) -> str:
        """
        Get a prompt template for complexity analysis.
        
        Args:
            provider: The AI provider to use
            research: Whether to use research mode
            
        Returns:
            The prompt template
        """
        if provider == "anthropic":
            return """
            Analyze the complexity of the following task:
            {{task}}
            
            Provide a detailed analysis in JSON format with:
            {
              "complexity": 1-10 score (1 being simplest),
              "recommendedSubtasks": recommended number of subtasks,
              "estimatedHours": total estimated hours,
              "analysis": detailed analysis of complexity factors,
              "riskFactors": array of potential risks,
              "suggestedApproach": recommended implementation approach
            }
            
            Consider:
            1. Technical complexity
            2. Integration requirements
            3. Testing needs
            4. Dependencies
            5. Potential risks
            """
        elif provider == "perplexity" and research:
            return """
            Analyze the complexity of the following task, incorporating industry knowledge and best practices:
            {{task}}
            
            Research similar implementations and provide:
            1. Complexity assessment
            2. Common pitfalls and solutions
            3. Industry standard approaches
            4. Reference architectures
            5. Recommended tools and frameworks
            6. Citations to relevant documentation
            
            Format your response as a JSON object with complexity metrics and detailed analysis.
            """
        else:
            return """
            Analyze the complexity of this task:
            {{task}}
            
            Format your response as a JSON object with complexity metrics and analysis.
            """
    
    def get_code_analysis_prompt(self, provider: str, research: bool = False, **kwargs: Any) -> str:
        """
        Get a prompt template for code analysis.
        
        Args:
            provider: The AI provider to use
            research: Whether to use research mode
            
        Returns:
            The prompt template
        """
        if provider == "anthropic":
            if research:
                return """
                Analyze the following code with thorough research and citations to industry standards:
                
                ```
                {{code}}
                ```
                
                Provide a comprehensive analysis including:
                1. In-depth explanation of what the code does and its underlying architecture
                2. Evaluation against current industry best practices and design patterns
                3. Identification of potential bugs, vulnerabilities, or code smells with references to coding standards
                4. Performance considerations with benchmark references where applicable
                5. Security implications with reference to OWASP or other security standards
                6. Detailed suggestions for improvement backed by research on modern approaches
                7. Code quality assessment with reference to established metrics
                
                Be specific in your analysis, reference line numbers where appropriate, and cite relevant
                documentation, articles, or research papers to support your assessment.
                """
            else:
                return """
                Analyze the following code:
                
                ```
                {{code}}
                ```
                
                Provide a detailed analysis including:
                1. Overview of what the code does
                2. Potential bugs or issues
                3. Performance considerations
                4. Security implications
                5. Suggestions for improvement
                6. Code quality assessment
                
                Be specific in your analysis and reference line numbers where appropriate.
                """
        elif provider == "perplexity":
            if research:
                return """
                Analyze the following code in the context of current best practices and industry standards, 
                leveraging up-to-date information and access to technical documentation:
                
                ```
                {{code}}
                ```
                
                Research and provide:
                1. Detailed explanation of the code's purpose, architecture, and functionality
                2. Analysis of the code structure, design patterns, and algorithm choices
                3. Comparison with industry best practices and latest recommended approaches
                4. Identification of anti-patterns, code smells, or technical debt
                5. Security vulnerability assessment with reference to current CVEs or security standards
                6. Performance optimization opportunities with quantitative metrics when possible
                7. Recommendations for modern alternatives, libraries, or improvements
                8. Insights on maintainability, scalability, and long-term viability
                
                Include:
                - Citations to relevant documentation, articles, GitHub issues, or research papers
                - References to similar implementations in popular open-source projects
                - Links to official language/framework documentation that supports your analysis
                - Examples of improved code patterns where appropriate
                - Mentions of relevant tools that could help address identified issues
                
                Your analysis should be thorough, evidence-based, and provide actionable insights
                that would meaningfully improve the code quality and adherence to current standards.
                """
            else:
                return """
                Analyze the following code in the context of current best practices and industry standards:
                
                ```
                {{code}}
                ```
                
                Research and provide:
                1. Detailed explanation of the code's purpose and functionality
                2. Analysis of the code architecture and design patterns used
                3. Comparison with industry best practices
                4. Identification of anti-patterns or code smells
                5. Security vulnerabilities assessment
                6. Performance optimization opportunities
                7. Recommendations for modern alternatives or improvements
                
                Include references to relevant documentation, articles, or research papers where applicable.
                """
        else:
            if research:
                return """
                Analyze this code with research-backed insights:
                
                ```
                {{code}}
                ```
                
                Provide a detailed analysis including explanation, issues, improvement suggestions,
                and references to relevant standards, documentation, or best practices.
                """
            else:
                return """
                Analyze this code:
                
                ```
                {{code}}
                ```
                
                Provide a detailed analysis including explanation, issues, and improvement suggestions.
                """
    
    def get_prd_parsing_prompt(self, provider: str, research: bool = False, **kwargs: Any) -> str:
        """
        Get a prompt template for PRD parsing.
        
        Args:
            provider: The AI provider to use
            research: Whether to use research mode
            
        Returns:
            The prompt template
        """
        if provider == "anthropic":
            if research:
                return """
                Analyze this Product Requirements Document (PRD) with thorough research on industry standards
                and best practices for task organization:
                
                {{prd_content}}
                
                Extract actionable engineering tasks and provide:
                1. A comprehensive breakdown of all requirements
                2. Industry-standard task organization following agile methodologies
                3. Critical path analysis with dependency identification
                4. Risk assessment with mitigation strategies for each task
                5. Implementation recommendations based on current best practices
                6. Estimated complexity with supporting rationale based on similar projects
                
                For each task, include:
                - Clear title and description
                - Priority with justification based on industry frameworks (e.g., MoSCoW, RICE)
                - Technical dependencies with rationale
                - Effort estimation with reference to similar components in comparable systems
                - Recommended approach with citations to best practices
                
                Format your response as a structured JSON array with comprehensive metadata.
                Include citations to relevant standards, methodologies, or case studies that inform your task breakdown.
                """
            else:
                return """
                Parse this Product Requirements Document (PRD) and extract actionable engineering tasks:
                
                {{prd_content}}
                
                For each task, include:
                - A clear title
                - Detailed description
                - Priority (high, medium, low)
                - Dependencies on other tasks
                - Estimated complexity (1-5)
                
                Format tasks as a structured JSON array with the following fields for each task:
                {
                  "id": "unique-id",
                  "title": "Task title",
                  "description": "Task description",
                  "priority": "high|medium|low",
                  "dependencies": ["id-of-dependency-1", "id-of-dependency-2"],
                  "complexity": 1-5 numerical value
                }
                """
        elif provider == "perplexity":
            if research:
                return """
                Analyze this Product Requirements Document (PRD) in the context of industry best practices, 
                and extract actionable engineering tasks:
                
                {{prd_content}}
                
                Research modern software development methodologies to:
                1. Extract core project requirements and objectives
                2. Identify specific technical capabilities needed
                3. Create a comprehensive breakdown of engineering tasks
                
                For each task, provide:
                - A clear title and description
                - Priority level with rationale
                - Recommended implementation approach based on industry standards
                - Potential challenges or technical considerations
                - Dependencies on other tasks
                - Estimated complexity (with justification)
                
                Format tasks as a structured JSON array that aligns with agile development practices.
                """
            else:
                return """
                Analyze this Product Requirements Document (PRD) and extract actionable engineering tasks:
                
                {{prd_content}}
                
                For each task, provide:
                - A clear title and description
                - Priority level
                - Dependencies on other tasks
                - Estimated complexity
                
                Format tasks as a structured JSON array following modern development practices.
                """
        else:
            if research:
                return """
                Parse this PRD and extract tasks with industry-standard organization:
                
                {{prd_content}}
                
                Research and provide a comprehensive task breakdown with references to best practices.
                Return a JSON array of tasks with detailed metadata and implementation recommendations.
                """
            else:
                return """
                Parse this PRD and extract tasks:
                
                {{prd_content}}
                
                Return a JSON array of tasks with title, description, priority, dependencies, and effort estimation.
                """
    
    def get_research_prompt(self, provider: str, research: bool = False, **kwargs: Any) -> str:
        """
        Get a prompt template for research operations.
        
        Args:
            provider: The AI provider to use
            research: Whether to use research mode
            
        Returns:
            The prompt template
        """
        if provider == "anthropic":
            if research:
                return """
                Research the following topic with comprehensive depth, providing thorough citations
                and evidence-based analysis:
                
                {{topic}}
                
                Provide an exhaustive analysis including:
                1. Comprehensive overview of the topic with historical context
                2. Current state-of-the-art with references to latest research or developments
                3. Key challenges, considerations, and open questions in the field
                4. Multiple competing methodologies or approaches with comparative analysis
                5. Best practices and recommendations based on empirical evidence
                6. Future trends and directions with supporting evidence
                7. Comprehensive bibliography of sources cited
                
                Your response should be thoroughly researched, critically evaluated,
                and supported by specific citations to authoritative sources.
                Where appropriate, include numerical data, metrics, or benchmarks.
                """
            else:
                return """
                Research the following topic in depth:
                
                {{topic}}
                
                Provide a comprehensive analysis including:
                1. Overview of the topic
                2. Current state-of-the-art
                3. Key challenges and considerations
                4. Best practices and recommendations
                5. Future trends and directions
                6. References to relevant resources
                
                Be thorough in your research and provide specific, actionable insights.
                """
        elif provider == "perplexity":
            if research:
                return """
                Research the following topic comprehensively, leveraging the most up-to-date information available:
                
                {{topic}}
                
                Provide:
                1. In-depth explanation of the topic
                2. Historical context and evolution
                3. Current state and latest developments
                4. Comparative analysis of different approaches
                5. Practical applications and limitations
                6. Expert opinions and controversies
                7. Future outlook and emerging trends
                
                Include citations to reputable sources, recent research papers, industry reports, and documentation.
                Where relevant, mention specific tools, libraries, frameworks, or technologies with version information.
                """
            else:
                return """
                Research the following topic with attention to current information:
                
                {{topic}}
                
                Provide:
                1. Clear explanation of the topic
                2. Current developments and state of the field
                3. Practical applications
                4. Key considerations and limitations
                5. Future directions
                
                Include references to relevant sources and documentation where applicable.
                """
        else:
            if research:
                return """
                Perform comprehensive research on this topic with citations:
                
                {{topic}}
                
                Provide a thorough analysis with specific details, evidence-based conclusions,
                and references to authoritative sources, current trends, and best practices.
                """
            else:
                return """
                Research this topic:
                
                {{topic}}
                
                Provide a comprehensive analysis with specific details and references.
                """
    
    def get_architecture_recommendation_prompt(self, provider: str, research: bool = False, **kwargs: Any) -> str:
        """
        Get a prompt template for architecture recommendations.
        
        Args:
            provider: The AI provider to use
            research: Whether to use research mode
            tech_stack: Optional dictionary with tech stack information
            codebase_summary: Optional string with codebase summary
            
        Returns:
            The prompt template
        """
        # Get tech stack and codebase summary from kwargs if available
        tech_stack = kwargs.get("tech_stack", {})
        codebase_summary = kwargs.get("codebase_summary", "")
        
        # Determine if this is for analyzing an existing codebase
        analyze_existing = kwargs.get("analyze_existing", False)
        
        if analyze_existing:
            # Templates for analyzing existing codebases
            if provider == "anthropic":
                if research:
                    return f"""
                    Analyze the architecture of the following codebase and recommend improvements 
                    based on industry standards and best practices:
                    
                    Codebase Summary:
                    {{{{codebase_summary}}}}
                    
                    {self._format_tech_stack(tech_stack)}
                    
                    Provide a comprehensive architecture analysis including:
                    1. Overall architecture assessment with strengths and weaknesses
                    2. Identification of architectural patterns in use and their appropriateness
                    3. Component relationships and potential coupling/cohesion issues
                    4. Scalability and performance bottlenecks with evidence
                    5. Security and maintainability concerns based on architectural choices
                    6. Specific architectural improvements with detailed justification
                    7. Migration path recommendations for implementing improvements
                    8. Architectural debt and technical risk assessment
                    
                    Include diagrams described in text format where appropriate.
                    Your analysis should be detailed, evidence-based, and grounded in software
                    architecture principles and design patterns. Cite specific examples from
                    the codebase where possible.
                    """
                else:
                    return f"""
                    Analyze the architecture of the following codebase and recommend improvements:
                    
                    Codebase Summary:
                    {{{{codebase_summary}}}}
                    
                    {self._format_tech_stack(tech_stack)}
                    
                    Provide a detailed architecture analysis including:
                    1. Overall architecture assessment
                    2. Identification of architectural patterns in use
                    3. Component relationships and dependencies
                    4. Scalability and performance considerations
                    5. Security and maintainability assessment
                    6. Specific improvement recommendations
                    
                    Include diagrams described in text format where appropriate.
                    Support your analysis with specific examples from the codebase.
                    """
            elif provider == "perplexity":
                if research:
                    return f"""
                    Analyze the architecture of the following codebase, research industry best practices, 
                    and recommend modern architectural improvements:
                    
                    Codebase Summary:
                    {{{{codebase_summary}}}}
                    
                    {self._format_tech_stack(tech_stack)}
                    
                    Research and provide:
                    1. Comprehensive architecture assessment with reference to architectural styles and patterns
                    2. Comparison of the current architecture with industry-standard approaches
                    3. Analysis of architectural constraints, technical debt, and quality attributes
                    4. Identification of anti-patterns with evidence from the codebase
                    5. Technology stack evaluation and modernization opportunities
                    6. Detailed recommendations for architectural evolution with references to similar systems
                    7. Implementation strategy with phased approach to minimize disruption
                    8. Modern practices from leading tech companies that could be applied
                    
                    Include references to academic papers, industry case studies, technical documentation, 
                    and real-world examples that support your recommendations. Cite specific examples from
                    the codebase where possible.
                    """
                else:
                    return f"""
                    Analyze the architecture of the following codebase and recommend improvements based on 
                    industry best practices:
                    
                    Codebase Summary:
                    {{{{codebase_summary}}}}
                    
                    {self._format_tech_stack(tech_stack)}
                    
                    Provide:
                    1. Comprehensive architecture assessment 
                    2. Identification of architectural patterns and anti-patterns
                    3. Technical debt and quality attribute analysis
                    4. Technology stack evaluation
                    5. Specific recommendations for architectural improvements
                    6. Implementation strategy
                    
                    Include references to documentation or examples where applicable.
                    """
            else:
                if research:
                    return f"""
                    Research and analyze the architecture of this codebase with citations to best practices:
                    
                    Codebase Summary:
                    {{{{codebase_summary}}}}
                    
                    {self._format_tech_stack(tech_stack)}
                    
                    Include architectural assessment, patterns identification, quality attributes analysis,
                    and detailed recommendations with references to relevant standards, frameworks, or patterns.
                    """
                else:
                    return f"""
                    Analyze the architecture of this codebase:
                    
                    Codebase Summary:
                    {{{{codebase_summary}}}}
                    
                    {self._format_tech_stack(tech_stack)}
                    
                    Include architectural assessment, patterns identification, and recommendations for improvement.
                    """
        else:
            # Templates for recommending new architecture based on requirements
            if provider == "anthropic":
                if research:
                    return """
                    Based on the following requirements, research and recommend an optimal architecture approach
                    with citations to industry standards and best practices:
                    
                    Requirements:
                    {{requirements}}
                    
                    Provide a comprehensive architecture recommendation including:
                    1. Overall architecture overview with research-backed rationale
                    2. Key components and their relationships with reference to design patterns
                    3. Technology stack recommendations with version compatibility considerations
                    4. Data flow and processing architecture with performance considerations
                    5. Scalability and performance considerations with reference to similar systems
                    6. Security and compliance approach citing relevant standards (e.g., OWASP, GDPR)
                    7. Testing and deployment strategy with modern CI/CD approaches
                    8. Maintenance considerations and future extensibility
                    
                    Include diagrams described in text format where appropriate.
                    Compare your recommended approach with alternatives, citing research, case studies,
                    or technical documentation that supports your recommendations.
                    """
                else:
                    return """
                    Based on the following requirements, recommend an architecture approach:
                    
                    Requirements:
                    {{requirements}}
                    
                    Provide a detailed architecture recommendation including:
                    1. Overall architecture overview and rationale
                    2. Key components and their relationships
                    3. Technology stack recommendations
                    4. Data flow and processing
                    5. Scalability and performance considerations
                    6. Security and compliance approach
                    7. Testing and deployment strategy
                    
                    Include diagrams described in text format where appropriate.
                    Explain the trade-offs of your recommended approach versus alternatives.
                    """
            elif provider == "perplexity":
                if research:
                    return """
                    Based on the following requirements, research and recommend a modern architecture approach 
                    that follows industry best practices:
                    
                    Requirements:
                    {{requirements}}
                    
                    Research and provide:
                    1. A comprehensive architecture recommendation with justification
                    2. Comparison of at least 3 potential architectural patterns that could address these requirements
                    3. Analysis of the pros, cons, and trade-offs for each approach
                    4. Technical stack recommendations with specific versions and compatibility considerations
                    5. Scalability strategy and performance optimization techniques
                    6. Security architecture and data protection measures
                    7. DevOps and CI/CD pipeline recommendations
                    8. Estimated implementation complexity and resource requirements
                    
                    Include references to case studies, technical documentation, and research papers 
                    that support your recommendations. Where possible, cite real-world examples of 
                    similar architectures in production systems.
                    """
                else:
                    return """
                    Based on the following requirements, recommend a modern architecture approach 
                    that follows industry best practices:
                    
                    Requirements:
                    {{requirements}}
                    
                    Provide:
                    1. A comprehensive architecture recommendation with justification
                    2. Analysis of potential architectural patterns
                    3. Technical stack recommendations with compatibility considerations
                    4. Scalability strategy and performance considerations
                    5. Security architecture and data protection measures
                    6. DevOps and CI/CD pipeline recommendations
                    
                    Include references to documentation or examples where applicable.
                    """
            else:
                if research:
                    return """
                    Research and recommend an architecture for these requirements with citations to best practices:
                    
                    {{requirements}}
                    
                    Include key components, technologies, data flow, implementation considerations,
                    and references to relevant standards, frameworks, or patterns that support your recommendations.
                    """
                else:
                    return """
                    Recommend an architecture for these requirements:
                    
                    {{requirements}}
                    
                    Include key components, technologies, data flow, and implementation considerations.
                    """
    
    def _format_tech_stack(self, tech_stack: Dict[str, Any]) -> str:
        """Format tech stack information for prompts."""
        if not tech_stack:
            return "Technology Stack: Not provided"
        
        result = ["Technology Stack:"]
        
        # Languages
        if "languages" in tech_stack:
            result.append("Languages:")
            for lang, stats in tech_stack.get("languages", {}).items():
                result.append(f"- {lang}")
        
        # Frameworks
        if "frameworks" in tech_stack:
            result.append("\nFrameworks:")
            for framework, details in tech_stack.get("frameworks", {}).items():
                version = details.get("version", "unknown version")
                result.append(f"- {framework} ({version})")
        
        # Libraries
        if "libraries" in tech_stack:
            result.append("\nLibraries:")
            for lib in tech_stack.get("libraries", []):
                result.append(f"- {lib}")
        
        # Package Managers
        if "package_managers" in tech_stack:
            result.append("\nPackages:")
            for pm, packages in tech_stack.get("package_managers", {}).items():
                for pkg, version in packages.items():
                    result.append(f"- {pkg} ({version})")
        
        return "\n".join(result)
    
    def get_code_generation_prompt(self, provider: str, research: bool = False, **kwargs: Any) -> str:
        """
        Get a prompt template for code generation.
        
        Args:
            provider: The AI provider to use
            research: Whether to use research mode
            
        Returns:
            The prompt template
        """
        if provider == "anthropic":
            return """
            Generate code based on the following requirements:
            
            {{requirements}}
            
            Language/Framework: {{language}}
            
            Provide:
            1. Complete, production-ready code
            2. Clear comments explaining key parts
            3. Error handling and edge cases
            4. Testing approach or example tests
            5. Instructions for integration
            
            The code should be:
            - Well-structured and modular
            - Following best practices for the specified language/framework
            - Secure and performant
            - Easy to understand and maintain
            """
        elif provider == "perplexity" and research:
            return """
            Generate high-quality code based on the following requirements, incorporating 
            current best practices and industry standards:
            
            {{requirements}}
            
            Language/Framework: {{language}}
            
            Research modern approaches to:
            1. Create efficient, secure, and maintainable code
            2. Implement the most appropriate design patterns
            3. Leverage current libraries and frameworks
            4. Follow industry-standard coding conventions
            
            Your solution should include:
            - Complete implementation with all necessary imports/dependencies
            - Comprehensive error handling and edge case management
            - Performance optimization considerations
            - Security best practices
            - Unit tests or testing strategy
            - Documentation following language-specific standards
            
            References to relevant documentation, examples, or GitHub repositories that demonstrate 
            similar approaches in real-world applications.
            """
        else:
            return """
            Generate code that meets these requirements:
            
            {{requirements}}
            
            Language/Framework: {{language}}
            
            Provide complete, well-structured code with appropriate error handling and comments.
            """ 