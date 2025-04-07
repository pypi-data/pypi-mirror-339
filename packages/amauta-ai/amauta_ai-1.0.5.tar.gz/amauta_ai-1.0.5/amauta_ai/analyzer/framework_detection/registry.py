"""
Framework detector registry.

This module provides a registry for framework detectors.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional, Type

from amauta_ai.analyzer.framework_detection.base import FrameworkDetector


class FrameworkDetectorRegistry:
    """
    Registry for framework detectors.
    
    This class maintains a registry of framework detectors and provides
    methods for registering and retrieving detectors.
    """
    
    def __init__(self):
        """Initialize the framework detector registry."""
        self._detectors: Dict[str, Type[FrameworkDetector]] = {}
        
    def register(self, detector_class: Type[FrameworkDetector]) -> None:
        """
        Register a framework detector.
        
        Args:
            detector_class: The detector class to register
        """
        # Create a temporary instance to get the language
        detector_instance = detector_class(Path("."))
        language = detector_instance.language
        
        self._detectors[language] = detector_class
        
    def get_detector(self, language: str, base_path: Path) -> Optional[FrameworkDetector]:
        """
        Get a detector for the specified language.
        
        Args:
            language: The language to get a detector for
            base_path: The base path of the project being analyzed
            
        Returns:
            A detector instance for the specified language, or None if not found
        """
        detector_class = self._detectors.get(language)
        if detector_class:
            return detector_class(base_path)
        return None
        
    def get_all_detectors(self, base_path: Path) -> List[FrameworkDetector]:
        """
        Get all registered detectors.
        
        Args:
            base_path: The base path of the project being analyzed
            
        Returns:
            A list of all registered detector instances
        """
        return [detector_class(base_path) for detector_class in self._detectors.values()]
        
    def detect_tech_stack(
        self,
        base_path: Path,
        files_by_extension: Dict[str, List[Path]],
        package_deps: Dict[str, Dict[str, Any]],
        use_ai: bool = False,
        ai_service = None
    ) -> Dict[str, List[str]]:
        """
        Detect the tech stack using all registered detectors.
        
        Args:
            base_path: The base path of the project being analyzed
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            use_ai: Whether to use AI assistance for detection
            ai_service: AI service to use for detection (if use_ai is True)
            
        Returns:
            A dictionary containing the detected tech stack
        """
        tech_stack = {
            "languages": [],
            "frameworks": [],
            "libraries": [],
            "tools": [],
        }
        
        # Get all detectors
        detectors = self.get_all_detectors(base_path)
        
        # If AI detection is enabled, add the AI detector
        if use_ai and ai_service:
            from amauta_ai.analyzer.framework_detection.base import AiFrameworkDetector
            detectors.append(AiFrameworkDetector(base_path, ai_service))
        
        # Detect languages (based on file extensions)
        languages = []
        for detector in detectors:
            if detector.is_language_present(files_by_extension):
                languages.append(detector.language)
                
        tech_stack["languages"] = languages
        
        # Detect frameworks, libraries, and tools
        frameworks = []
        libraries = []
        tools = []
        
        for detector in detectors:
            if detector.is_language_present(files_by_extension) or detector.language == "AI-Enhanced":
                frameworks.extend(detector.detect_frameworks(files_by_extension, package_deps))
                libraries.extend(detector.detect_libraries(files_by_extension, package_deps))
                tools.extend(detector.detect_tools(files_by_extension, package_deps))
                
        # Remove duplicates while preserving order
        tech_stack["frameworks"] = list(dict.fromkeys(frameworks))
        tech_stack["libraries"] = list(dict.fromkeys(libraries))
        tech_stack["tools"] = list(dict.fromkeys(tools))
        
        return tech_stack


# Create a singleton instance
_registry = FrameworkDetectorRegistry()

def register(detector_class: Type[FrameworkDetector]) -> Type[FrameworkDetector]:
    """
    Decorator for registering a framework detector.
    
    Args:
        detector_class: The detector class to register
        
    Returns:
        The detector class (unchanged)
    """
    _registry.register(detector_class)
    return detector_class

def get_registry() -> FrameworkDetectorRegistry:
    """
    Get the singleton registry instance.
    
    Returns:
        The singleton registry instance
    """
    return _registry 