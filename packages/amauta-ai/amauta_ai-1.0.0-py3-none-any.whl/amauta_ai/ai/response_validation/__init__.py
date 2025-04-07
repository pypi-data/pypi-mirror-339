"""
Response validation framework for AI model outputs.

This module provides a comprehensive validation framework for AI model responses,
ensuring consistent, well-structured, and reliable outputs across the AMAUTA platform.
The framework supports validation schemas for different response types, error recovery
strategies, and utility functions for common validation tasks.
"""

from typing import Any, Dict, List, Optional, Type, Union, Callable
import json
import re
import logging
from enum import Enum
from pydantic import BaseModel, Field, ValidationError

logger = logging.getLogger(__name__)

class ResponseValidationError(Exception):
    """Base exception for response validation errors."""
    
    def __init__(
        self, 
        message: str, 
        raw_response: str = "", 
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the exception.
        
        Args:
            message: The error message
            raw_response: The raw AI response that failed validation
            details: Additional details about the error
        """
        self.raw_response = raw_response
        self.details = details or {}
        super().__init__(message)


class ValidationStrategy(str, Enum):
    """Strategy for handling validation failures."""
    
    STRICT = "strict"  # Raise exception on validation failure
    REPAIR = "repair"  # Attempt to repair invalid responses
    FALLBACK = "fallback"  # Use fallback values on validation failure


class ResponseFormat(str, Enum):
    """Format of the AI response."""
    
    JSON = "json"  # JSON format
    TEXT = "text"  # Plain text
    MARKDOWN = "markdown"  # Markdown format
    CODE = "code"  # Code snippet


class BaseResponseValidator:
    """Base class for all response validators."""
    
    def __init__(
        self, 
        expected_format: ResponseFormat = ResponseFormat.JSON,
        strategy: ValidationStrategy = ValidationStrategy.REPAIR
    ):
        """
        Initialize the validator.
        
        Args:
            expected_format: The expected format of the response
            strategy: The validation strategy to use
        """
        self.expected_format = expected_format
        self.strategy = strategy
    
    def validate(self, response: str) -> Any:
        """
        Validate a response.
        
        Args:
            response: The raw response string from the AI model
            
        Returns:
            The validated response (format depends on validator type)
            
        Raises:
            ResponseValidationError: If validation fails and strategy is STRICT
        """
        raise NotImplementedError("Subclasses must implement validate method")
    
    def extract_format(self, response: str) -> str:
        """
        Extract the relevant part of the response based on expected format.
        
        Args:
            response: The raw response string
            
        Returns:
            The extracted content
        """
        if not response:
            return ""
            
        if self.expected_format == ResponseFormat.JSON:
            # Try to extract JSON from code blocks or directly
            json_pattern = r"```(?:json)?\s*([\s\S]*?)```"
            matches = re.findall(json_pattern, response)
            
            if matches:
                return matches[0].strip()
            
            # Try to find a JSON object or array
            json_pattern = r"(\{[\s\S]*\}|\[[\s\S]*\])"
            matches = re.findall(json_pattern, response)
            
            if matches:
                return matches[0].strip()
                
            return response.strip()
            
        elif self.expected_format == ResponseFormat.CODE:
            # Extract code from code blocks
            code_pattern = r"```(?:[a-zA-Z]+)?\s*([\s\S]*?)```"
            matches = re.findall(code_pattern, response)
            
            if matches:
                return matches[0].strip()
                
            return response.strip()
            
        elif self.expected_format == ResponseFormat.MARKDOWN:
            # Return as is for markdown
            return response.strip()
            
        else:
            # Plain text - strip any markdown code blocks
            text = re.sub(r"```[\s\S]*?```", "", response)
            return text.strip()


class SchemaValidator(BaseResponseValidator):
    """
    Validator that uses a Pydantic model schema to validate responses.
    
    This validator ensures that AI responses match a predefined schema
    with appropriate data types and constraints.
    """
    
    def __init__(
        self, 
        schema_model: Type[BaseModel],
        fallback_generator: Optional[Callable[[], Dict[str, Any]]] = None,
        expected_format: ResponseFormat = ResponseFormat.JSON,
        strategy: ValidationStrategy = ValidationStrategy.REPAIR
    ):
        """
        Initialize the schema validator.
        
        Args:
            schema_model: The Pydantic model to use for validation
            fallback_generator: Optional function to generate fallback values
            expected_format: The expected format of the response
            strategy: The validation strategy to use
        """
        super().__init__(expected_format, strategy)
        self.schema_model = schema_model
        self.fallback_generator = fallback_generator
    
    def validate(self, response: str) -> Union[BaseModel, Dict[str, Any]]:
        """
        Validate a response against the schema.
        
        Args:
            response: The raw response string
            
        Returns:
            The validated model instance or dictionary
            
        Raises:
            ResponseValidationError: If validation fails and strategy is STRICT
        """
        if not response:
            if self.strategy == ValidationStrategy.STRICT:
                raise ResponseValidationError("Empty response")
            elif self.strategy == ValidationStrategy.FALLBACK and self.fallback_generator:
                return self.schema_model(**self.fallback_generator())
            else:
                # Try to create an instance with default values
                try:
                    return self.schema_model()
                except ValidationError:
                    raise ResponseValidationError("Empty response and no fallback available")
        
        # Extract the relevant part of the response
        extracted = self.extract_format(response)
        
        try:
            # Try to parse as JSON
            if self.expected_format == ResponseFormat.JSON:
                try:
                    data = json.loads(extracted)
                except json.JSONDecodeError as e:
                    if self.strategy == ValidationStrategy.STRICT:
                        raise ResponseValidationError(
                            f"Invalid JSON: {str(e)}", 
                            raw_response=response
                        )
                    elif self.strategy == ValidationStrategy.FALLBACK and self.fallback_generator:
                        return self.schema_model(**self.fallback_generator())
                    else:
                        # Try repair - look for simpler JSON patterns
                        raise ResponseValidationError(
                            "JSON parsing failed and repair not implemented", 
                            raw_response=response
                        )
            else:
                # Non-JSON formats require custom parsing logic
                # For now we just use the extracted text as is
                data = {"content": extracted}
            
            # Validate against the schema
            try:
                validated = self.schema_model(**data)
                return validated
            except ValidationError as e:
                if self.strategy == ValidationStrategy.STRICT:
                    raise ResponseValidationError(
                        f"Schema validation failed: {str(e)}", 
                        raw_response=response,
                        details={"validation_errors": e.errors()}
                    )
                elif self.strategy == ValidationStrategy.REPAIR:
                    # Try to repair the data by adding missing fields with defaults
                    repaired_data = self._repair_data(data, e)
                    return self.schema_model(**repaired_data)
                elif self.fallback_generator:
                    return self.schema_model(**self.fallback_generator())
                else:
                    raise ResponseValidationError(
                        "Validation failed and no fallback available", 
                        raw_response=response
                    )
                    
        except Exception as e:
            if isinstance(e, ResponseValidationError):
                raise
            else:
                raise ResponseValidationError(
                    f"Unexpected error during validation: {str(e)}", 
                    raw_response=response
                )
    
    def _repair_data(self, data: Dict[str, Any], validation_error: ValidationError) -> Dict[str, Any]:
        """
        Attempt to repair invalid data by filling in missing fields.
        
        Args:
            data: The data that failed validation
            validation_error: The validation error
            
        Returns:
            Repaired data dictionary
        """
        repaired = data.copy()
        
        # Extract field information from the schema
        schema_fields = {
            field_name: (field.annotation, field.default, field.default_factory)
            for field_name, field in self.schema_model.__annotations__.items()
        }
        
        # Extract errors by field
        error_fields = {}
        for error in validation_error.errors():
            field_path = error["loc"][0] if error["loc"] else ""
            error_fields[field_path] = error
        
        # Add missing fields or fix invalid ones
        for field_name, (type_annotation, default, default_factory) in schema_fields.items():
            if field_name in error_fields or field_name not in repaired:
                # Field is missing or invalid
                if default is not None:
                    repaired[field_name] = default
                elif default_factory is not None:
                    repaired[field_name] = default_factory()
                else:
                    # Try to infer a reasonable default based on type
                    if type_annotation == str:
                        repaired[field_name] = ""
                    elif type_annotation == int:
                        repaired[field_name] = 0
                    elif type_annotation == float:
                        repaired[field_name] = 0.0
                    elif type_annotation == bool:
                        repaired[field_name] = False
                    elif type_annotation == list or type_annotation == List:
                        repaired[field_name] = []
                    elif type_annotation == dict or type_annotation == Dict:
                        repaired[field_name] = {}
                    else:
                        # Can't infer a default
                        repaired[field_name] = None
        
        return repaired


class JsonValidator(BaseResponseValidator):
    """
    Validator that ensures responses are valid JSON and match certain criteria.
    
    This validator is less strict than SchemaValidator but ensures that the
    response is valid JSON and optionally has required fields.
    """
    
    def __init__(
        self,
        required_fields: Optional[List[str]] = None,
        expected_format: ResponseFormat = ResponseFormat.JSON,
        strategy: ValidationStrategy = ValidationStrategy.REPAIR
    ):
        """
        Initialize the JSON validator.
        
        Args:
            required_fields: Optional list of fields that must be present
            expected_format: The expected format of the response
            strategy: The validation strategy to use
        """
        super().__init__(expected_format, strategy)
        self.required_fields = required_fields or []
    
    def validate(self, response: str) -> Dict[str, Any]:
        """
        Validate that a response is valid JSON with required fields.
        
        Args:
            response: The raw response string
            
        Returns:
            The parsed JSON data
            
        Raises:
            ResponseValidationError: If validation fails and strategy is STRICT
        """
        if not response:
            if self.strategy == ValidationStrategy.STRICT:
                raise ResponseValidationError("Empty response")
            else:
                # Return empty dict or one with required fields
                result = {}
                for field in self.required_fields:
                    result[field] = None
                return result
        
        # Extract the relevant part of the response
        extracted = self.extract_format(response)
        
        try:
            # Try to parse as JSON
            data = json.loads(extracted)
            
            # Check for required fields
            missing_fields = [field for field in self.required_fields if field not in data]
            
            if missing_fields and self.strategy == ValidationStrategy.STRICT:
                raise ResponseValidationError(
                    f"Missing required fields: {', '.join(missing_fields)}",
                    raw_response=response
                )
            
            # Add missing fields if needed
            if missing_fields and self.strategy == ValidationStrategy.REPAIR:
                for field in missing_fields:
                    data[field] = None
            
            return data
            
        except json.JSONDecodeError as e:
            if self.strategy == ValidationStrategy.STRICT:
                raise ResponseValidationError(
                    f"Invalid JSON: {str(e)}", 
                    raw_response=response
                )
            elif self.strategy == ValidationStrategy.REPAIR:
                # Try to repair by finding JSON-like structures
                return self._repair_json(response)
            else:
                # Return empty dict or one with required fields
                result = {}
                for field in self.required_fields:
                    result[field] = None
                return result
    
    def _repair_json(self, response: str) -> Dict[str, Any]:
        """
        Attempt to repair invalid JSON.
        
        Args:
            response: The raw response string
            
        Returns:
            Repaired JSON dictionary
        """
        # Try to find JSON-like structures
        json_pattern = r"(\{[\s\S]*?\}|\[[\s\S]*?\])"
        matches = re.findall(json_pattern, response)
        
        for match in matches:
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
        
        # If no valid JSON found, create a basic structure
        result = {}
        for field in self.required_fields:
            result[field] = None
            
        # Try to extract key-value pairs from the text
        kv_pattern = r"['\"]([\w\s]+)['\"]:\s*['\"]?([\w\s]+)['\"]?"
        kv_matches = re.findall(kv_pattern, response)
        
        for key, value in kv_matches:
            result[key.strip()] = value.strip()
            
        return result


class TextValidator(BaseResponseValidator):
    """
    Validator for text responses that ensures they meet certain criteria.
    
    This validator checks text responses for length, content patterns,
    and other text-specific validation rules.
    """
    
    def __init__(
        self,
        min_length: int = 0,
        max_length: Optional[int] = None,
        required_patterns: Optional[List[str]] = None,
        forbidden_patterns: Optional[List[str]] = None,
        expected_format: ResponseFormat = ResponseFormat.TEXT,
        strategy: ValidationStrategy = ValidationStrategy.REPAIR
    ):
        """
        Initialize the text validator.
        
        Args:
            min_length: Minimum allowed length
            max_length: Maximum allowed length (None for no limit)
            required_patterns: Regex patterns that must be present
            forbidden_patterns: Regex patterns that must not be present
            expected_format: The expected format of the response
            strategy: The validation strategy to use
        """
        super().__init__(expected_format, strategy)
        self.min_length = min_length
        self.max_length = max_length
        self.required_patterns = required_patterns or []
        self.forbidden_patterns = forbidden_patterns or []
    
    def validate(self, response: str) -> str:
        """
        Validate a text response.
        
        Args:
            response: The raw response string
            
        Returns:
            The validated text
            
        Raises:
            ResponseValidationError: If validation fails and strategy is STRICT
        """
        if not response:
            if self.strategy == ValidationStrategy.STRICT:
                raise ResponseValidationError("Empty response")
            else:
                return ""
        
        # Extract the relevant part of the response
        text = self.extract_format(response)
        
        # Check length
        if len(text) < self.min_length:
            if self.strategy == ValidationStrategy.STRICT:
                raise ResponseValidationError(
                    f"Response too short: {len(text)} < {self.min_length}",
                    raw_response=response
                )
            elif self.strategy == ValidationStrategy.REPAIR:
                # Cannot repair short responses
                pass
            
        if self.max_length and len(text) > self.max_length:
            if self.strategy == ValidationStrategy.STRICT:
                raise ResponseValidationError(
                    f"Response too long: {len(text)} > {self.max_length}",
                    raw_response=response
                )
            elif self.strategy == ValidationStrategy.REPAIR:
                text = text[:self.max_length]
        
        # Check required patterns
        for pattern in self.required_patterns:
            if not re.search(pattern, text):
                if self.strategy == ValidationStrategy.STRICT:
                    raise ResponseValidationError(
                        f"Missing required pattern: {pattern}",
                        raw_response=response
                    )
                # Cannot repair missing patterns
        
        # Check forbidden patterns
        for pattern in self.forbidden_patterns:
            if re.search(pattern, text):
                if self.strategy == ValidationStrategy.STRICT:
                    raise ResponseValidationError(
                        f"Contains forbidden pattern: {pattern}",
                        raw_response=response
                    )
                elif self.strategy == ValidationStrategy.REPAIR:
                    text = re.sub(pattern, "", text)
        
        return text


# Export commonly used validators
__all__ = [
    "ResponseValidationError",
    "ValidationStrategy",
    "ResponseFormat",
    "BaseResponseValidator",
    "SchemaValidator",
    "JsonValidator",
    "TextValidator",
] 