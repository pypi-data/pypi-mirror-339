"""
Web technologies framework detector.

This module provides a detector for web technologies (HTML, CSS, etc).
"""

from pathlib import Path
from typing import Dict, List, Any

from amauta_ai.analyzer.framework_detection.base import FrameworkDetector
from amauta_ai.analyzer.framework_detection.registry import register


@register
class WebTechnologiesDetector(FrameworkDetector):
    """
    Detector for web technologies.
    
    This detector identifies HTML, CSS, and related web technologies
    based on file types and content patterns.
    """
    
    @property
    def language(self) -> str:
        """
        Get the language this detector handles.
        
        Returns:
            The name of the language this detector handles
        """
        return "Web"
        
    def is_language_present(self, files_by_extension: Dict[str, List[Path]]) -> bool:
        """
        Check if web technologies are present in the codebase.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            
        Returns:
            True if web technologies are present, False otherwise
        """
        web_extensions = [".html", ".htm", ".css", ".scss", ".sass", ".less"]
        return any(ext in files_by_extension for ext in web_extensions)
        
    def detect_frameworks(
        self,
        files_by_extension: Dict[str, List[Path]],
        package_deps: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """
        Detect web frameworks.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected frameworks
        """
        frameworks = []
        
        # Collect HTML files
        html_files = []
        for ext in [".html", ".htm"]:
            if ext in files_by_extension:
                html_files.extend(files_by_extension[ext])
                
        # Check for CSS frameworks in Node dependencies
        node_deps = package_deps["node"]["dependencies"]
        node_dev_deps = package_deps["node"]["devDependencies"]
        
        # Framework mapping from package.json
        framework_mapping = {
            "bootstrap": "Bootstrap",
            "tailwindcss": "Tailwind CSS",
            "bulma": "Bulma",
            "foundation-sites": "Foundation",
            "materialize-css": "Materialize CSS",
            "semantic-ui": "Semantic UI",
            "@material/web": "Material Web Components",
            "lit-element": "Lit Element",
            "lit-html": "Lit HTML",
            "polymer": "Polymer",
            "@webcomponents/webcomponentsjs": "Web Components",
            "jquery": "jQuery",
            "alpinejs": "Alpine.js",
            "stimulus": "Stimulus",
            "@hotwired/stimulus": "Stimulus",
            "@hotwired/turbo": "Turbo",
        }
        
        # Check dependencies
        for dep, framework in framework_mapping.items():
            if dep in node_deps or dep in node_dev_deps:
                if framework not in frameworks:
                    frameworks.append(framework)
                    
        # Detect web frameworks from HTML content
        if html_files:
            framework_patterns = {
                "Bootstrap": [
                    r'<link[^>]*bootstrap.*\.css',
                    r'<script[^>]*bootstrap.*\.js',
                    r'class="[^"]*btn[^"]*"',
                    r'class="[^"]*container[^"]*"',
                    r'class="[^"]*row[^"]*"',
                    r'class="[^"]*col-[^"]*"',
                ],
                "Tailwind CSS": [
                    r'class="[^"]*bg-blue-[^"]*"',
                    r'class="[^"]*text-[a-z]+-[0-9]+[^"]*"',
                    r'class="[^"]*flex[^"]*"',
                    r'class="[^"]*grid[^"]*"',
                    r'class="[^"]*p-[0-9]+[^"]*"',
                    r'class="[^"]*m-[0-9]+[^"]*"',
                ],
                "Foundation": [
                    r'<link[^>]*foundation.*\.css',
                    r'<script[^>]*foundation.*\.js',
                    r'class="[^"]*button[^"]*"',
                    r'class="[^"]*grid-x[^"]*"',
                    r'class="[^"]*cell[^"]*"',
                ],
                "Materialize CSS": [
                    r'<link[^>]*materialize.*\.css',
                    r'<script[^>]*materialize.*\.js',
                    r'class="[^"]*waves-effect[^"]*"',
                    r'class="[^"]*card[^"]*"',
                ],
                "Bulma": [
                    r'<link[^>]*bulma.*\.css',
                    r'class="[^"]*columns[^"]*"',
                    r'class="[^"]*column[^"]*"',
                    r'class="[^"]*notification[^"]*"',
                ],
                "jQuery": [
                    r'<script[^>]*jquery.*\.js',
                    r'\$\(.+\)',
                    r'jQuery\(.+\)',
                ],
                "Alpine.js": [
                    r'<script[^>]*alpine.*\.js',
                    r'x-data',
                    r'x-bind',
                    r'x-on',
                    r'x-show',
                ],
                "Web Components": [
                    r'customElements\.define',
                    r'class\s+\w+\s+extends\s+HTMLElement',
                    r'attachShadow',
                    r'<template\s',
                ],
            }
            
            # Run pattern analysis
            pattern_results = self.analyze_file_patterns(html_files, framework_patterns)
            
            # Add detected frameworks
            for framework in pattern_results:
                if framework not in frameworks:
                    frameworks.append(framework)
                    
        return frameworks
        
    def detect_libraries(
        self,
        files_by_extension: Dict[str, List[Path]],
        package_deps: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """
        Detect web libraries.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected libraries
        """
        libraries = []
        
        # Check for libraries in Node dependencies
        node_deps = package_deps["node"]["dependencies"]
        node_dev_deps = package_deps["node"]["devDependencies"]
        
        # Library mapping from package.json
        library_mapping = {
            "d3": "D3.js",
            "chart.js": "Chart.js",
            "three": "Three.js",
            "leaflet": "Leaflet",
            "mapbox-gl": "Mapbox GL",
            "hammer.js": "Hammer.js",
            "gsap": "GSAP",
            "anime.js": "Anime.js",
            "howler": "Howler.js",
            "tone": "Tone.js",
            "marked": "Marked",
            "highlight.js": "Highlight.js",
            "prismjs": "Prism.js",
            "moment": "Moment.js",
            "luxon": "Luxon",
            "date-fns": "date-fns",
            "dropzone": "Dropzone.js",
            "sortablejs": "Sortable.js",
            "simplebar": "SimpleBar",
            "pdfjs-dist": "PDF.js",
            "quill": "Quill",
            "codemirror": "CodeMirror",
            "monaco-editor": "Monaco Editor",
            "dompurify": "DOMPurify",
            "sanitize-html": "sanitize-html",
        }
        
        # Check dependencies
        for dep, library in library_mapping.items():
            if dep in node_deps or dep in node_dev_deps:
                if library not in libraries:
                    libraries.append(library)
                    
        # Collect HTML files for pattern detection
        html_files = []
        for ext in [".html", ".htm"]:
            if ext in files_by_extension:
                html_files.extend(files_by_extension[ext])
                
        # Detect libraries from HTML content
        if html_files:
            library_patterns = {
                "D3.js": [
                    r'<script[^>]*d3.*\.js',
                    r'd3\.select',
                    r'd3\.scale',
                    r'd3\.svg',
                ],
                "Chart.js": [
                    r'<script[^>]*chart.*\.js',
                    r'new\s+Chart\(',
                ],
                "Three.js": [
                    r'<script[^>]*three.*\.js',
                    r'THREE\.',
                    r'new\s+THREE\.',
                ],
                "Leaflet": [
                    r'<script[^>]*leaflet.*\.js',
                    r'<link[^>]*leaflet.*\.css',
                    r'L\.map\(',
                    r'L\.tileLayer\(',
                ],
                "GSAP": [
                    r'<script[^>]*gsap.*\.js',
                    r'TweenMax',
                    r'TweenLite',
                    r'gsap\.',
                ],
                "CodeMirror": [
                    r'<script[^>]*codemirror.*\.js',
                    r'<link[^>]*codemirror.*\.css',
                    r'CodeMirror\(',
                ],
            }
            
            # Run pattern analysis
            pattern_results = self.analyze_file_patterns(html_files, library_patterns)
            
            # Add detected libraries
            for library in pattern_results:
                if library not in libraries:
                    libraries.append(library)
                    
        return libraries
        
    def detect_tools(
        self,
        files_by_extension: Dict[str, List[Path]],
        package_deps: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """
        Detect web tools.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected tools
        """
        tools = []
        
        # Check for tools in Node dependencies
        node_deps = package_deps["node"]["dependencies"]
        node_dev_deps = package_deps["node"]["devDependencies"]
        
        # Tool mapping from package.json
        tool_mapping = {
            "postcss": "PostCSS",
            "autoprefixer": "Autoprefixer",
            "sass": "Sass",
            "node-sass": "Sass",
            "less": "Less",
            "stylus": "Stylus",
            "purgecss": "PurgeCSS",
            "cssnano": "CSSnano",
            "html-minifier": "HTML Minifier",
            "terser": "Terser",
            "uglify-js": "UglifyJS",
            "browserify": "Browserify",
            "esbuild": "esbuild",
            "snowpack": "Snowpack",
            "lighthouse": "Lighthouse",
            "pwa-asset-generator": "PWA Asset Generator",
            "workbox-cli": "Workbox",
            "browser-sync": "Browser Sync",
            "serve": "Serve",
            "live-server": "Live Server",
            "htmlhint": "HTMLHint",
            "stylelint": "Stylelint",
            "pug": "Pug",
            "handlebars": "Handlebars",
            "mustache": "Mustache",
            "ejs": "EJS",
        }
        
        # Check dependencies
        for dep, tool in tool_mapping.items():
            if dep in node_deps or dep in node_dev_deps:
                if tool not in tools:
                    tools.append(tool)
                    
        # Check for configuration files that indicate tool usage
        config_files = {
            ".postcssrc": "PostCSS",
            "postcss.config.js": "PostCSS",
            ".stylelintrc": "Stylelint",
            "stylelint.config.js": "Stylelint",
            ".browserslistrc": "Browserslist",
            ".pug-lintrc": "Pug Lint",
            "purgecss.config.js": "PurgeCSS",
            "workbox-config.js": "Workbox",
        }
        
        for config_file, tool in config_files.items():
            if (self.base_path / config_file).exists():
                if tool not in tools:
                    tools.append(tool)
                    
        return tools 