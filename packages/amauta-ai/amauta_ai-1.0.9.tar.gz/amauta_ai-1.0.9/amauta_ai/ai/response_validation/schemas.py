"""
Response validation schemas for AI model outputs.

This module provides Pydantic model schemas for validating different types
of AI model responses used throughout the AMAUTA platform.
"""

from typing import Any, Dict, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field, validator
from datetime import datetime


class TaskComplexityLevel(str, Enum):
    """Complexity level for task complexity analysis."""
    
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskTimeEstimate(BaseModel):
    """Time estimate for task completion."""
    
    hours: float = Field(default=0, ge=0, description="Estimated hours")
    confidence: float = Field(default=0.5, ge=0, le=1, description="Confidence level (0-1)")


class TaskComplexityAnalysis(BaseModel):
    """
    Schema for task complexity analysis responses.
    
    Used to validate AI responses when analyzing task complexity.
    """
    
    complexity_score: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Complexity score from 1-10"
    )
    
    risk_level: TaskComplexityLevel = Field(
        default=TaskComplexityLevel.MEDIUM,
        description="Overall risk level"
    )
    
    time_estimate: TaskTimeEstimate = Field(
        default_factory=TaskTimeEstimate,
        description="Estimated time to complete"
    )
    
    key_factors: List[str] = Field(
        default_factory=list,
        description="Key factors contributing to complexity"
    )
    
    technical_challenges: List[str] = Field(
        default_factory=list,
        description="Technical challenges to consider"
    )
    
    dependencies: List[str] = Field(
        default_factory=list,
        description="Dependencies affecting complexity"
    )
    
    rationale: str = Field(
        default="",
        description="Explanation for the complexity assessment"
    )
    
    @validator("complexity_score")
    def complexity_score_valid(cls, v: int) -> int:
        """Ensure complexity score is within valid range."""
        if v < 1 or v > 10:
            return 5
        return v
    
    @validator("key_factors")
    def key_factors_not_empty(cls, v: List[str]) -> List[str]:
        """Ensure key factors list is not empty."""
        if not v:
            return ["Task scope", "Implementation complexity"]
        return v


class ExpandedTaskItem(BaseModel):
    """
    Schema for expanded task items.
    
    Used to validate subtasks generated during task expansion.
    """
    
    title: str = Field(..., description="Task title")
    description: str = Field(default="", description="Task description")
    priority: str = Field(default="medium", description="Task priority")
    type: str = Field(default="task", description="Task type")
    
    @validator("title")
    def title_not_empty(cls, v: str) -> str:
        """Ensure title is not empty."""
        if not v:
            raise ValueError("Title cannot be empty")
        return v
    
    @validator("priority")
    def priority_valid(cls, v: str) -> str:
        """Ensure priority is valid."""
        valid_priorities = ["low", "medium", "high", "critical"]
        if v.lower() not in valid_priorities:
            return "medium"
        return v.lower()
    
    @validator("type")
    def type_valid(cls, v: str) -> str:
        """Ensure type is valid."""
        valid_types = ["task", "story", "epic", "issue"]
        if v.lower() not in valid_types:
            return "task"
        return v.lower()


class TaskGenerationResult(BaseModel):
    """
    Schema for task generation results.
    
    Used to validate AI responses when generating tasks from requirements.
    """
    
    tasks: List[ExpandedTaskItem] = Field(
        default_factory=list,
        description="Generated tasks"
    )
    
    @validator("tasks")
    def tasks_not_empty(cls, v: List[ExpandedTaskItem]) -> List[ExpandedTaskItem]:
        """Ensure tasks list is not empty."""
        if not v:
            # Create a default task if none are provided
            return [
                ExpandedTaskItem(
                    title="Default Task",
                    description="This task was created as a fallback because no valid tasks were generated.",
                    priority="medium",
                    type="task"
                )
            ]
        return v


class CodeGenerationResponse(BaseModel):
    """
    Schema for code generation responses.
    
    Used to validate AI responses when generating code.
    """
    
    code: str = Field(..., description="Generated code")
    explanation: str = Field(default="", description="Explanation of the generated code")
    imports: List[str] = Field(default_factory=list, description="Required imports")
    dependencies: List[str] = Field(default_factory=list, description="External dependencies")
    language: str = Field(default="python", description="Programming language")
    
    @validator("code")
    def code_not_empty(cls, v: str) -> str:
        """Ensure code is not empty."""
        if not v:
            raise ValueError("Code cannot be empty")
        return v
    
    @validator("language")
    def language_valid(cls, v: str) -> str:
        """Ensure language is supported."""
        supported_languages = [
            "python", "javascript", "typescript", "java", "c", "cpp", "csharp",
            "go", "rust", "php", "ruby", "shell", "sql", "html", "css"
        ]
        if v.lower() not in supported_languages:
            return "python"
        return v.lower()


class DocumentationGenerationResponse(BaseModel):
    """
    Schema for documentation generation responses.
    
    Used to validate AI responses when generating documentation.
    """
    
    content: str = Field(..., description="Generated documentation content")
    title: str = Field(default="", description="Documentation title")
    format: str = Field(default="markdown", description="Documentation format")
    sections: List[str] = Field(default_factory=list, description="Section titles")
    
    @validator("content")
    def content_not_empty(cls, v: str) -> str:
        """Ensure content is not empty."""
        if not v:
            raise ValueError("Documentation content cannot be empty")
        return v
    
    @validator("format")
    def format_valid(cls, v: str) -> str:
        """Ensure format is valid."""
        valid_formats = ["markdown", "rst", "html", "text"]
        if v.lower() not in valid_formats:
            return "markdown"
        return v.lower()


class AnalysisResult(BaseModel):
    """
    Base schema for analysis results.
    
    Used as a base for various analysis responses.
    """
    
    timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")
    source: str = Field(default="amauta-ai", description="Analysis source")
    confidence: float = Field(default=0.8, ge=0, le=1, description="Confidence level (0-1)")


class SecurityVulnerabilityLevel(str, Enum):
    """Security vulnerability level."""
    
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SecurityVulnerability(BaseModel):
    """Security vulnerability details."""
    
    type: str = Field(..., description="Vulnerability type")
    description: str = Field(..., description="Vulnerability description")
    severity: SecurityVulnerabilityLevel = Field(
        default=SecurityVulnerabilityLevel.MEDIUM,
        description="Vulnerability severity"
    )
    mitigation: str = Field(default="", description="Mitigation strategy")
    affected_components: List[str] = Field(default_factory=list, description="Affected components")


class SecurityAnalysisResponse(AnalysisResult):
    """
    Schema for security analysis responses.
    
    Used to validate AI responses when performing security analysis.
    """
    
    vulnerabilities: List[SecurityVulnerability] = Field(
        default_factory=list,
        description="Identified vulnerabilities"
    )
    
    overall_risk: SecurityVulnerabilityLevel = Field(
        default=SecurityVulnerabilityLevel.LOW,
        description="Overall security risk"
    )
    
    recommendations: List[str] = Field(
        default_factory=list,
        description="Security recommendations"
    )
    
    @validator("overall_risk")
    def calculate_overall_risk(cls, v: SecurityVulnerabilityLevel, values: Dict[str, Any]) -> SecurityVulnerabilityLevel:
        """Calculate overall risk based on vulnerabilities if not provided."""
        # If overall risk was explicitly set and vulnerabilities exist, use it
        if v != SecurityVulnerabilityLevel.LOW or "vulnerabilities" not in values:
            return v
            
        # Calculate based on vulnerabilities
        vulnerabilities = values["vulnerabilities"]
        if not vulnerabilities:
            return SecurityVulnerabilityLevel.NONE
            
        # Check for critical vulnerabilities
        if any(vuln.severity == SecurityVulnerabilityLevel.CRITICAL for vuln in vulnerabilities):
            return SecurityVulnerabilityLevel.CRITICAL
            
        # Check for high vulnerabilities
        if any(vuln.severity == SecurityVulnerabilityLevel.HIGH for vuln in vulnerabilities):
            return SecurityVulnerabilityLevel.HIGH
            
        # Check for medium vulnerabilities
        if any(vuln.severity == SecurityVulnerabilityLevel.MEDIUM for vuln in vulnerabilities):
            return SecurityVulnerabilityLevel.MEDIUM
            
        # Check for low vulnerabilities
        if any(vuln.severity == SecurityVulnerabilityLevel.LOW for vuln in vulnerabilities):
            return SecurityVulnerabilityLevel.LOW
            
        return SecurityVulnerabilityLevel.NONE


class PRDParsingResponse(BaseModel):
    """
    Schema for PRD parsing responses.
    
    Used to validate AI responses when parsing Product Requirements Documents.
    """
    
    tasks: List[ExpandedTaskItem] = Field(
        default_factory=list,
        description="Generated tasks from PRD"
    )
    
    epics: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Epic-level items identified"
    )
    
    features: List[str] = Field(
        default_factory=list,
        description="Features identified in the PRD"
    )
    
    requirements: List[str] = Field(
        default_factory=list,
        description="Key requirements identified"
    )
    
    stakeholders: List[str] = Field(
        default_factory=list,
        description="Stakeholders mentioned in the PRD"
    )
    
    @validator("tasks")
    def tasks_not_empty(cls, v: List[ExpandedTaskItem]) -> List[ExpandedTaskItem]:
        """Ensure tasks list is not empty."""
        if not v:
            # Create a default task if none are provided
            return [
                ExpandedTaskItem(
                    title="Review Requirements",
                    description="Review the requirements document to identify tasks.",
                    priority="high",
                    type="task"
                )
            ]
        return v


# Export the schemas
__all__ = [
    "TaskComplexityLevel",
    "TaskTimeEstimate",
    "TaskComplexityAnalysis",
    "ExpandedTaskItem",
    "TaskGenerationResult",
    "CodeGenerationResponse",
    "DocumentationGenerationResponse",
    "AnalysisResult",
    "SecurityVulnerabilityLevel",
    "SecurityVulnerability",
    "SecurityAnalysisResponse",
    "PRDParsingResponse"
] 