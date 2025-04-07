"""
Integration of response validation framework with AMAUTA AI components.

This module provides integration points between the response validation framework
and existing AMAUTA AI components, allowing for easy adoption across the platform.
"""

import logging
import functools
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, cast

from amauta_ai.ai.service import AiService
from amauta_ai.ai.command_base import AiCommandBase

from amauta_ai.ai.response_validation import (
    ResponseValidationError,
    ValidationStrategy,
    BaseResponseValidator,
    SchemaValidator,
    JsonValidator,
    TextValidator,
)

from amauta_ai.ai.response_validation.utils import (
    validate_task_complexity_analysis,
    validate_task_expansion,
    validate_code_generation,
    validate_security_analysis,
    validate_prd_parsing,
)

from amauta_ai.ai.response_validation.schemas import (
    TaskComplexityAnalysis,
    ExpandedTaskItem,
    CodeGenerationResponse,
    SecurityAnalysisResponse,
    PRDParsingResponse,
)

logger = logging.getLogger(__name__)

# Type variable for generic functions
T = TypeVar("T")


def validate_ai_response(
    response_type: str,
    response: str,
    strategy: ValidationStrategy = ValidationStrategy.REPAIR
) -> Any:
    """
    Validate an AI response based on its type.
    
    Args:
        response_type: The type of response to validate
        response: The raw response string
        strategy: The validation strategy to use
        
    Returns:
        Validated response object
        
    Raises:
        ResponseValidationError: If validation fails and strategy is STRICT
        ValueError: If response_type is unknown
    """
    # Map response types to validation functions
    validation_map = {
        "task_complexity": validate_task_complexity_analysis,
        "task_expansion": validate_task_expansion,
        "code_generation": validate_code_generation,
        "security_analysis": validate_security_analysis,
        "prd_parsing": validate_prd_parsing,
    }
    
    if response_type not in validation_map:
        raise ValueError(f"Unknown response type: {response_type}")
    
    # Get the appropriate validation function
    validation_func = validation_map[response_type]
    
    # Call the validation function
    return validation_func(response, strategy)


def with_response_validation(
    response_type: str,
    strategy: ValidationStrategy = ValidationStrategy.REPAIR
) -> Callable[[Callable[..., str]], Callable[..., Any]]:
    """
    Decorator to apply response validation to a function.
    
    Args:
        response_type: The type of response to validate
        strategy: The validation strategy to use
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable[..., str]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Call the original function to get the response
            response = func(*args, **kwargs)
            
            # Validate the response
            try:
                return validate_ai_response(response_type, response, strategy)
            except ResponseValidationError as e:
                # Log the error
                logger.error(f"Response validation error: {e}")
                
                # Re-raise if strategy is STRICT, otherwise return the raw response
                if strategy == ValidationStrategy.STRICT:
                    raise
                
                return response
                
        return wrapper
    return decorator


def patch_ai_service(ai_service: AiService) -> None:
    """
    Patch an AiService instance to use response validation.
    
    This function adds response validation to key methods of the AiService class.
    
    Args:
        ai_service: The AiService instance to patch
    """
    # Store original methods
    original_query_anthropic_with_thinking = ai_service.query_anthropic_with_thinking
    original_expand_task = ai_service.expand_task
    
    # Patch methods with validation
    @functools.wraps(original_query_anthropic_with_thinking)
    def patched_query_anthropic_with_thinking(*args: Any, **kwargs: Any) -> Dict[str, Any]:
        response = original_query_anthropic_with_thinking(*args, **kwargs)
        # Try to validate as task complexity analysis
        try:
            validated = validate_task_complexity_analysis(
                str(response), ValidationStrategy.REPAIR
            )
            # Convert pydantic model to dict
            return validated.model_dump()
        except Exception as e:
            logger.warning(f"Error validating task complexity analysis: {e}")
            return response
    
    @functools.wraps(original_expand_task)
    def patched_expand_task(*args: Any, **kwargs: Any) -> List[Dict[str, str]]:
        response = original_expand_task(*args, **kwargs)
        # Try to convert response to string if needed
        response_str = str(response) if not isinstance(response, str) else response
        
        # Try to validate as task expansion
        try:
            validated_tasks = validate_task_expansion(response_str, ValidationStrategy.REPAIR)
            # Convert pydantic models to dicts
            return [task.model_dump() for task in validated_tasks]
        except Exception as e:
            logger.warning(f"Error validating task expansion: {e}")
            return response
    
    # Apply patches
    ai_service.query_anthropic_with_thinking = patched_query_anthropic_with_thinking  # type: ignore
    ai_service.expand_task = patched_expand_task  # type: ignore


def patch_ai_command_base(command_class: Type[AiCommandBase[Any]]) -> Type[AiCommandBase[Any]]:
    """
    Patch an AiCommandBase subclass to use response validation.
    
    This function returns a new class that adds response validation to the
    parse_json_response method of the AiCommandBase class.
    
    Args:
        command_class: The AiCommandBase subclass to patch
        
    Returns:
        Patched AiCommandBase subclass
    """
    # Store original method
    original_parse_json_response = command_class.parse_json_response
    
    # Patch method with validation
    @functools.wraps(original_parse_json_response)
    def patched_parse_json_response(self: AiCommandBase[Any], response: str) -> Any:
        try:
            # Try original method first
            result = original_parse_json_response(self, response)
            return result
        except Exception as e:
            logger.warning(f"Error in original parse_json_response: {e}")
            
            # Try to validate with JsonValidator as fallback
            try:
                validator = JsonValidator(strategy=ValidationStrategy.REPAIR)
                validated = validator.validate(response)
                return validated
            except Exception as inner_e:
                logger.error(f"Error in fallback JSON validation: {inner_e}")
                # Re-raise original exception
                raise e
    
    # Create a new class with the patched method
    class PatchedCommandClass(command_class):  # type: ignore
        parse_json_response = patched_parse_json_response
    
    # Copy over class attributes
    PatchedCommandClass.__name__ = f"Validated{command_class.__name__}"
    PatchedCommandClass.__doc__ = command_class.__doc__
    
    return PatchedCommandClass


def create_validated_ai_service() -> AiService:
    """
    Create an AiService instance with validation enabled.
    
    Returns:
        AiService instance with validation
    """
    # Create a normal AiService
    ai_service = AiService()
    
    # Patch it with validation
    patch_ai_service(ai_service)
    
    return ai_service


# Export integration functions
__all__ = [
    "validate_ai_response",
    "with_response_validation",
    "patch_ai_service",
    "patch_ai_command_base",
    "create_validated_ai_service",
] 