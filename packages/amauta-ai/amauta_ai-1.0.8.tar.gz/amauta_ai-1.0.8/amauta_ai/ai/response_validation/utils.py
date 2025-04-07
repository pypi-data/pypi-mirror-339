"""
Utility functions for AI response validation.

This module provides helper functions for common response validation tasks,
including JSON extraction, repair strategies, and integration with the AMAUTA
response validation framework.
"""

import json
import re
import logging
from typing import Any, Dict, List, Optional, Type, Union

from pydantic import BaseModel, ValidationError

from amauta_ai.ai.response_validation import (
    ResponseValidationError,
    ValidationStrategy,
    BaseResponseValidator,
    SchemaValidator,
    JsonValidator,
)

from amauta_ai.ai.response_validation.schemas import (
    TaskComplexityAnalysis,
    ExpandedTaskItem,
    TaskGenerationResult,
    CodeGenerationResponse,
    SecurityAnalysisResponse,
    PRDParsingResponse,
)

logger = logging.getLogger(__name__)


def extract_json_from_response(response: str) -> Optional[Dict[str, Any]]:
    """
    Extract JSON from a response string.
    
    Args:
        response: The raw response string
        
    Returns:
        Extracted JSON as a dictionary or None if extraction fails
    """
    if not response:
        return None
        
    # Try direct parsing first
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        pass
        
    # Try to extract JSON from code blocks
    json_pattern = r"```(?:json)?\s*([\s\S]*?)```"
    matches = re.findall(json_pattern, response)
    
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    # Try to find any JSON-like structure surrounded by {} or []
    json_pattern = r"(\{[\s\S]*\}|\[[\s\S]*\])"
    matches = re.findall(json_pattern, response)
    
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    return None


def validate_task_complexity_analysis(
    response: str,
    strategy: ValidationStrategy = ValidationStrategy.REPAIR
) -> TaskComplexityAnalysis:
    """
    Validate a task complexity analysis response.
    
    Args:
        response: The raw response string
        strategy: The validation strategy to use
        
    Returns:
        Validated TaskComplexityAnalysis instance
        
    Raises:
        ResponseValidationError: If validation fails and strategy is STRICT
    """
    validator = SchemaValidator(
        schema_model=TaskComplexityAnalysis,
        strategy=strategy,
        fallback_generator=lambda: {
            "complexity_score": 5,
            "risk_level": "medium",
            "key_factors": ["Task scope", "Implementation complexity"],
            "time_estimate": {"hours": 8, "confidence": 0.5},
        }
    )
    
    return validator.validate(response)


def validate_task_expansion(
    response: str,
    strategy: ValidationStrategy = ValidationStrategy.REPAIR
) -> List[ExpandedTaskItem]:
    """
    Validate a task expansion response.
    
    Args:
        response: The raw response string
        strategy: The validation strategy to use
        
    Returns:
        List of validated ExpandedTaskItem instances
        
    Raises:
        ResponseValidationError: If validation fails and strategy is STRICT
    """
    try:
        # Try to extract JSON from the response
        json_data = extract_json_from_response(response)
        
        if json_data is None:
            raise ResponseValidationError("Could not extract JSON from response")
        
        # Check if JSON is a list of tasks or a TaskGenerationResult
        if isinstance(json_data, list):
            # Create a TaskGenerationResult with the task list
            json_data = {"tasks": json_data}
        
        # Validate using the schema
        validator = SchemaValidator(
            schema_model=TaskGenerationResult,
            strategy=strategy
        )
        
        result = validator.validate(json.dumps(json_data))
        
        # Return the tasks list
        return result.tasks
        
    except (ResponseValidationError, Exception) as e:
        if strategy == ValidationStrategy.STRICT:
            if isinstance(e, ResponseValidationError):
                raise
            else:
                raise ResponseValidationError(f"Failed to validate task expansion: {str(e)}")
        
        # For non-strict strategies, try to extract tasks manually
        fallback_tasks = _extract_fallback_tasks(response)
        
        if not fallback_tasks and strategy == ValidationStrategy.FALLBACK:
            # Create a default task
            return [
                ExpandedTaskItem(
                    title="Review Expansion",
                    description="The AI-generated task expansion could not be properly parsed. Please review the original response and create tasks manually.",
                    priority="medium",
                    type="task"
                )
            ]
        
        return fallback_tasks


def validate_code_generation(
    response: str,
    strategy: ValidationStrategy = ValidationStrategy.REPAIR
) -> CodeGenerationResponse:
    """
    Validate a code generation response.
    
    Args:
        response: The raw response string
        strategy: The validation strategy to use
        
    Returns:
        Validated CodeGenerationResponse instance
        
    Raises:
        ResponseValidationError: If validation fails and strategy is STRICT
    """
    # Extract code blocks first
    code_pattern = r"```(?:[a-zA-Z]+)?\s*([\s\S]*?)```"
    code_matches = re.findall(code_pattern, response)
    
    # If we have code blocks, try to build a valid response
    if code_matches:
        code = code_matches[0]
        
        # Try to determine language from the code block
        language = "python"  # Default
        language_pattern = r"```([a-zA-Z]+)\s"
        language_matches = re.findall(language_pattern, response)
        if language_matches:
            language = language_matches[0].lower()
        
        # Extract explanation (text before or after code block)
        code_block_pattern = r"```[a-zA-Z]*\s[\s\S]*?```"
        explanation = re.sub(code_block_pattern, "", response).strip()
        
        # Create a dictionary for validation
        data = {
            "code": code,
            "explanation": explanation,
            "language": language
        }
        
        # Try to extract imports from the code if it's Python
        if language == "python":
            imports = []
            import_pattern = r"(?:^|\n)(?:import|from)\s+([^\s]+)"
            import_matches = re.findall(import_pattern, code)
            if import_matches:
                imports = import_matches
            data["imports"] = imports
        
        json_data = json.dumps(data)
    else:
        # No code blocks found, try to see if it's a JSON response
        json_data = response
    
    # Validate using the schema
    validator = SchemaValidator(
        schema_model=CodeGenerationResponse,
        strategy=strategy
    )
    
    try:
        return validator.validate(json_data)
    except ResponseValidationError:
        if strategy == ValidationStrategy.STRICT:
            raise
        
        # For REPAIR strategy, try to extract code manually
        code = ""
        for match in code_matches:
            if match:
                code = match
                break
        
        if not code:
            # No code blocks found, use the entire response
            code = response
        
        return CodeGenerationResponse(
            code=code,
            explanation="",
            language="python"
        )


def validate_security_analysis(
    response: str,
    strategy: ValidationStrategy = ValidationStrategy.REPAIR
) -> SecurityAnalysisResponse:
    """
    Validate a security analysis response.
    
    Args:
        response: The raw response string
        strategy: The validation strategy to use
        
    Returns:
        Validated SecurityAnalysisResponse instance
        
    Raises:
        ResponseValidationError: If validation fails and strategy is STRICT
    """
    validator = SchemaValidator(
        schema_model=SecurityAnalysisResponse,
        strategy=strategy
    )
    
    try:
        return validator.validate(response)
    except ResponseValidationError:
        if strategy == ValidationStrategy.STRICT:
            raise
        
        # For non-strict strategies, try to extract vulnerabilities
        vulnerabilities = []
        
        # Look for patterns like "Vulnerability: Description"
        vuln_pattern = r"(?:Vulnerability|Issue|Problem|Risk):\s*([^\n]+)"
        vuln_matches = re.findall(vuln_pattern, response, re.IGNORECASE)
        
        for i, match in enumerate(vuln_matches):
            vulnerabilities.append({
                "type": f"Vulnerability {i+1}",
                "description": match.strip(),
                "severity": "medium"
            })
        
        # Look for recommendations
        recommendations = []
        rec_pattern = r"(?:Recommendation|Suggestion|Fix|Mitigation):\s*([^\n]+)"
        rec_matches = re.findall(rec_pattern, response, re.IGNORECASE)
        
        for match in rec_matches:
            recommendations.append(match.strip())
        
        # Create a basic response
        return SecurityAnalysisResponse(
            vulnerabilities=vulnerabilities,
            recommendations=recommendations,
            overall_risk="medium" if vulnerabilities else "low"
        )


def validate_prd_parsing(
    response: str,
    strategy: ValidationStrategy = ValidationStrategy.REPAIR
) -> PRDParsingResponse:
    """
    Validate a PRD parsing response.
    
    Args:
        response: The raw response string
        strategy: The validation strategy to use
        
    Returns:
        Validated PRDParsingResponse instance
        
    Raises:
        ResponseValidationError: If validation fails and strategy is STRICT
    """
    validator = SchemaValidator(
        schema_model=PRDParsingResponse,
        strategy=strategy
    )
    
    try:
        return validator.validate(response)
    except ResponseValidationError:
        if strategy == ValidationStrategy.STRICT:
            raise
        
        # For non-strict strategies, try to extract tasks
        tasks = _extract_fallback_tasks(response)
        
        # Extract features
        features = []
        feature_pattern = r"(?:Feature|Functionality):\s*([^\n]+)"
        feature_matches = re.findall(feature_pattern, response, re.IGNORECASE)
        features.extend(match.strip() for match in feature_matches)
        
        # Extract requirements
        requirements = []
        req_pattern = r"(?:Requirement|Spec):\s*([^\n]+)"
        req_matches = re.findall(req_pattern, response, re.IGNORECASE)
        requirements.extend(match.strip() for match in req_matches)
        
        # Create a basic response
        return PRDParsingResponse(
            tasks=tasks,
            features=features,
            requirements=requirements
        )


def _extract_fallback_tasks(response: str) -> List[ExpandedTaskItem]:
    """
    Extract tasks from a response when validation fails.
    
    Args:
        response: The raw response string
        
    Returns:
        List of ExpandedTaskItem instances
    """
    tasks = []
    
    # Look for task patterns like "Task: Description"
    task_pattern = r"(?:Task|Story|Epic|Issue):\s*([^\n]+)"
    task_matches = re.findall(task_pattern, response, re.IGNORECASE)
    
    for i, match in enumerate(task_matches):
        try:
            tasks.append(ExpandedTaskItem(
                title=match.strip(),
                description=f"Task {i+1} extracted from response",
                priority="medium",
                type="task"
            ))
        except ValidationError:
            continue
    
    return tasks


# Export utility functions
__all__ = [
    "extract_json_from_response",
    "validate_task_complexity_analysis",
    "validate_task_expansion",
    "validate_code_generation",
    "validate_security_analysis",
    "validate_prd_parsing",
] 