"""
Base framework detection classes.

This module defines the base classes for framework detection.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Any, Set, Optional


class FrameworkDetector(ABC):
    """
    Base class for all framework detectors.
    
    The FrameworkDetector hierarchy provides a flexible way to detect frameworks
    across different programming languages. Each detector is responsible for
    identifying frameworks for a specific language or technology.
    """

    def __init__(self, base_path: Path):
        """
        Initialize the framework detector.
        
        Args:
            base_path: The base path of the project being analyzed
        """
        self.base_path = base_path
        
    @property
    @abstractmethod
    def language(self) -> str:
        """
        Get the language this detector handles.
        
        Returns:
            The name of the language this detector handles
        """
        pass
        
    @abstractmethod
    def detect_frameworks(
        self,
        files_by_extension: Dict[str, List[Path]],
        package_deps: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """
        Detect frameworks for the specified language.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected frameworks
        """
        pass
        
    @abstractmethod
    def detect_libraries(
        self,
        files_by_extension: Dict[str, List[Path]],
        package_deps: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """
        Detect libraries for the specified language.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected libraries
        """
        pass

    @abstractmethod
    def detect_tools(
        self,
        files_by_extension: Dict[str, List[Path]],
        package_deps: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """
        Detect tools for the specified language.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected tools
        """
        pass
        
    def is_language_present(self, files_by_extension: Dict[str, List[Path]]) -> bool:
        """
        Check if the language handled by this detector is present in the codebase.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            
        Returns:
            True if the language is present, False otherwise
        """
        # This is a default implementation that should be overridden 
        # by specific language detectors if necessary
        return False
        
    def analyze_file_patterns(
        self, 
        files: List[Path],
        pattern_sets: Dict[str, List[str]]
    ) -> Set[str]:
        """
        Analyze files for patterns that indicate framework usage.
        
        Args:
            files: List of files to analyze
            pattern_sets: Dictionary mapping framework names to lists of regex patterns
            
        Returns:
            Set of framework names whose patterns were found
        """
        import re
        
        detected_frameworks = set()
        
        for file_path in files:
            if not file_path.exists():
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                    # Check each framework's patterns
                    for framework, patterns in pattern_sets.items():
                        for pattern in patterns:
                            if re.search(pattern, content, re.MULTILINE):
                                detected_frameworks.add(framework)
                                break  # No need to check other patterns for this framework
            except Exception:
                # Skip files that can't be read
                continue
                
        return detected_frameworks


class AiFrameworkDetector(FrameworkDetector):
    """
    Framework detector that uses AI to identify frameworks.
    
    This detector uses the Anthropic API to analyze code patterns and identify
    frameworks that may not be explicitly declared in dependency files.
    """
    
    def __init__(self, base_path: Path, ai_service=None):
        """
        Initialize the AI framework detector.
        
        Args:
            base_path: The base path of the project being analyzed
            ai_service: Optional AI service to use for detection
        """
        super().__init__(base_path)
        self.ai_service = ai_service
        
    @property
    def language(self) -> str:
        """
        Get the language this detector handles.
        
        Returns:
            The name of the language this detector handles
        """
        return "AI-Enhanced"
        
    def detect_frameworks(
        self,
        files_by_extension: Dict[str, List[Path]],
        package_deps: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """
        Detect frameworks using AI analysis.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected frameworks
        """
        # If no AI service is provided, return an empty list
        if not self.ai_service:
            return []
            
        # Prepare a sample of files to analyze
        code_samples = self._extract_code_samples(files_by_extension)
        if not code_samples:
            return []
            
        # Use AI to detect frameworks
        return self._analyze_with_ai(code_samples, "frameworks")
        
    def detect_libraries(
        self,
        files_by_extension: Dict[str, List[Path]],
        package_deps: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """
        Detect libraries using AI analysis.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected libraries
        """
        # If no AI service is provided, return an empty list
        if not self.ai_service:
            return []
            
        # Prepare a sample of files to analyze
        code_samples = self._extract_code_samples(files_by_extension)
        if not code_samples:
            return []
            
        # Use AI to detect libraries
        return self._analyze_with_ai(code_samples, "libraries")
        
    def detect_tools(
        self,
        files_by_extension: Dict[str, List[Path]],
        package_deps: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """
        Detect tools using AI analysis.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected tools
        """
        # If no AI service is provided, return an empty list
        if not self.ai_service:
            return []
            
        # For tools, we'll look at configuration files more than code
        config_files = self._extract_config_files(files_by_extension)
        if not config_files:
            return []
            
        # Use AI to detect tools
        return self._analyze_with_ai(config_files, "tools")
        
    def is_language_present(self, files_by_extension: Dict[str, List[Path]]) -> bool:
        """
        Check if the language handled by this detector is present in the codebase.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            
        Returns:
            True if the language is present, False otherwise
        """
        # AI detector works with any language
        return bool(files_by_extension)
        
    def _extract_code_samples(self, files_by_extension: Dict[str, List[Path]]) -> str:
        """
        Extract a representative sample of code files for AI analysis.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            
        Returns:
            String containing code samples
        """
        samples = []
        max_files_per_ext = 3  # Limit to keep the prompt size manageable
        max_lines_per_file = 100
        
        for ext, files in files_by_extension.items():
            # Skip non-code files
            if ext not in ['.py', '.js', '.jsx', '.ts', '.tsx', '.rb', '.php', '.go', '.rs']:
                continue
                
            # Take a sample of files for each extension
            for file_path in files[:max_files_per_ext]:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.readlines()[:max_lines_per_file]
                        
                    samples.append(f"--- File: {file_path.name} ---\n")
                    samples.append("".join(content))
                    samples.append("\n\n")
                except Exception:
                    # Skip files that can't be read
                    continue
                    
        return "".join(samples)
        
    def _extract_config_files(self, files_by_extension: Dict[str, List[Path]]) -> str:
        """
        Extract configuration files for AI analysis.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            
        Returns:
            String containing configuration file content
        """
        config_files = []
        
        # Look for common configuration files
        config_paths = [
            self.base_path / "package.json",
            self.base_path / "requirements.txt",
            self.base_path / "Gemfile",
            self.base_path / "composer.json",
            self.base_path / "go.mod",
            self.base_path / "Cargo.toml",
            self.base_path / ".eslintrc",
            self.base_path / ".prettierrc",
            self.base_path / "pyproject.toml",
            self.base_path / "tox.ini",
            self.base_path / ".github/workflows",
            self.base_path / "Dockerfile",
            self.base_path / "docker-compose.yml",
        ]
        
        for path in config_paths:
            if path.exists() and path.is_file():
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    config_files.append(f"--- File: {path.name} ---\n")
                    config_files.append(content)
                    config_files.append("\n\n")
                except Exception:
                    # Skip files that can't be read
                    continue
                    
        return "".join(config_files)
        
    def _analyze_with_ai(self, code_sample: str, detection_type: str) -> List[str]:
        """
        Use AI to analyze code and detect frameworks/libraries/tools.
        
        Args:
            code_sample: String containing code samples
            detection_type: Type of technology to detect (frameworks, libraries, tools)
            
        Returns:
            List of detected technologies
        """
        if not self.ai_service or not code_sample:
            return []
            
        # Create a prompt for AI analysis
        prompt = f"""Analyze the following code and identify the {detection_type} being used.
        
Focus on detecting {detection_type} only. Return your answer as a comma-separated list.

{code_sample}

{detection_type.capitalize()} detected (comma-separated list):"""

        try:
            # Use the AI service to analyze the code
            response = self.ai_service.generate_text(prompt)
            
            # Parse the response to extract detected technologies
            if response:
                # Extract comma-separated items, clean up each item
                items = [item.strip() for item in response.split(',')]
                # Remove any empty items
                items = [item for item in items if item]
                return items
        except Exception:
            # If AI analysis fails, return an empty list
            pass
            
        return [] 