"""
Configuration models for AMAUTA.

This module defines the configuration models used throughout AMAUTA,
including AI provider configuration, task settings, and general preferences.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

from pydantic import BaseModel, Field


class AiProviderType(str, Enum):
    """Type of AI provider."""

    ANTHROPIC = "anthropic"
    PERPLEXITY = "perplexipy"


class ProviderCapability(str, Enum):
    """Provider capabilities."""

    GENERAL = "general"
    RESEARCH = "research"
    CODE = "code"
    TASK = "task"
    ANALYSIS = "analysis"
    STREAMING = "streaming"
    TOOL_CALLS = "tool_calls"
    FUNCTION_CALLING = "function_calling"
    VISION = "vision"
    LONG_CONTEXT = "long_context"
    RAG = "rag"


class ModelMetadata(BaseModel):
    """Metadata about a specific model offered by a provider."""

    name: str
    context_window: int = Field(default=16000, description="Maximum context window size in tokens")
    max_tokens_out: int = Field(default=4000, description="Maximum output tokens")
    supports_vision: bool = Field(default=False, description="Whether the model supports vision/image inputs")
    supports_tools: bool = Field(default=False, description="Whether the model supports tool calls/function calling")
    recommended_for: List[str] = Field(
        default_factory=list,
        description="Operation types this model is recommended for (e.g., 'general', 'code', 'research')"
    )


class AiProviderConfig(BaseModel):
    """Configuration for an AI provider."""

    provider: AiProviderType
    default_model: str
    api_key_env_var: str = Field(
        description="Name of the environment variable containing the API key"
    )
    capabilities: Optional[Set[ProviderCapability]] = Field(
        default=None,
        description="Set of capabilities this provider supports"
    )
    models: Optional[Dict[str, ModelMetadata]] = Field(
        default=None,
        description="Metadata about models available from this provider"
    )
    base_url: Optional[str] = Field(
        default=None,
        description="Optional base URL override for the provider API"
    )
    version: Optional[str] = Field(
        default=None, 
        description="Provider library version or compatibility information"
    )
    timeout_seconds: int = Field(
        default=60,
        description="Timeout in seconds for API calls to this provider"
    )
    retry_attempts: int = Field(
        default=2,
        description="Number of retry attempts for failed API calls"
    )

    class Config:
        """Pydantic model configuration."""
        json_encoders = {
            AiProviderType: lambda v: v.value,
            ProviderCapability: lambda v: v.value,
            set: lambda v: list(v) if v is not None else None,
        }


class ProviderPreferences(BaseModel):
    """Provider preferences for different operation modes."""

    general: List[str] = Field(
        default_factory=lambda: ["anthropic", "perplexipy"],
        description="Ordered list of preferred providers for general operations"
    )
    research: List[str] = Field(
        default_factory=lambda: ["perplexipy", "anthropic"],
        description="Ordered list of preferred providers for research operations"
    )
    code: List[str] = Field(
        default_factory=lambda: ["anthropic", "perplexipy"],
        description="Ordered list of preferred providers for code operations"
    )
    analysis: List[str] = Field(
        default_factory=lambda: ["anthropic", "perplexipy"],
        description="Ordered list of preferred providers for analysis operations"
    )
    task: List[str] = Field(
        default_factory=lambda: ["anthropic", "perplexipy"],
        description="Ordered list of preferred providers for task management operations"
    )


class ResearchModeConfig(BaseModel):
    """Configuration for research mode."""
    
    enabled_by_default: bool = Field(
        default=False,
        description="Whether research mode is enabled by default (can be overridden by --research flag)"
    )
    preferred_providers: List[str] = Field(
        default_factory=lambda: ["perplexipy", "anthropic"],
        description="Ordered list of preferred providers specifically for research operations"
    )
    context_boost: bool = Field(
        default=True,
        description="Whether to boost context window size when in research mode"
    )
    required_capabilities: List[ProviderCapability] = Field(
        default_factory=lambda: [ProviderCapability.RESEARCH, ProviderCapability.LONG_CONTEXT],
        description="Capabilities required for research mode providers"
    )
    prompt_templates: Dict[str, str] = Field(
        default_factory=dict,
        description="Specialized prompt templates for research mode operations"
    )


class ProjectConfig(BaseModel):
    """Project configuration."""

    name: str = Field(description="Project name")
    description: str = Field(description="Project description")
    repository: Optional[str] = Field(default=None, description="Project repository URL")
    coding_standards: Dict[str, Any] = Field(
        default_factory=lambda: {
            "python": {
                "style_guide": "PEP 8",
                "type_hints": True,
                "docstrings": True,
                "linters": ["black", "mypy", "ruff"]
            }
        },
        description="Project coding standards"
    )


class AnalyzerConfig(BaseModel):
    """Code analyzer configuration."""

    ignored_paths: List[str] = Field(
        default_factory=lambda: [
            "node_modules",
            "venv",
            ".venv",
            "dist",
            "build",
            "__pycache__",
            ".git",
        ],
        description="Paths to ignore during analysis"
    )
    languages: List[str] = Field(
        default_factory=lambda: ["python", "javascript", "typescript"],
        description="Languages to analyze"
    )
    max_file_size_kb: int = Field(
        default=1024, description="Maximum file size to analyze in KB"
    )


class AmautarcConfig(BaseModel):
    """Root configuration for .amautarc.yaml."""

    project: ProjectConfig = Field(default_factory=ProjectConfig)
    analyzer: AnalyzerConfig = Field(default_factory=AnalyzerConfig)
    ai: Dict[str, AiProviderConfig] = Field(
        default_factory=dict, description="AI provider configurations"
    )
    provider_preferences: ProviderPreferences = Field(
        default_factory=ProviderPreferences,
        description="Provider preferences for different operation modes"
    )
    research_mode: ResearchModeConfig = Field(
        default_factory=ResearchModeConfig,
        description="Configuration for research mode"
    )
    log_level: str = Field(default="INFO", description="Logging level")
    custom_rules: Dict[str, Any] = Field(
        default_factory=dict, description="Custom rules for .cursorrules generation"
    )
