"""
JavaScript framework detector.

This module provides a detector for JavaScript frameworks and libraries.
"""

from pathlib import Path
from typing import Dict, List, Any

from amauta_ai.analyzer.framework_detection.base import FrameworkDetector
from amauta_ai.analyzer.framework_detection.registry import register


@register
class JavaScriptFrameworkDetector(FrameworkDetector):
    """
    Detector for JavaScript frameworks and libraries.
    
    This detector identifies JavaScript/TypeScript frameworks, libraries,
    and tools based on package dependencies and code patterns.
    """
    
    @property
    def language(self) -> str:
        """
        Get the language this detector handles.
        
        Returns:
            The name of the language this detector handles
        """
        return "JavaScript"
        
    def is_language_present(self, files_by_extension: Dict[str, List[Path]]) -> bool:
        """
        Check if JavaScript/TypeScript is present in the codebase.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            
        Returns:
            True if JavaScript/TypeScript is present, False otherwise
        """
        js_extensions = [".js", ".jsx", ".ts", ".tsx"]
        return any(ext in files_by_extension for ext in js_extensions)
        
    def detect_frameworks(
        self,
        files_by_extension: Dict[str, List[Path]],
        package_deps: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """
        Detect JavaScript frameworks.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected frameworks
        """
        frameworks = []
        
        # Check for frameworks in package dependencies
        node_deps = package_deps["node"]["dependencies"]
        node_dev_deps = package_deps["node"]["devDependencies"]
        
        # Framework detection based on package.json dependencies
        framework_mapping = {
            "react": "React",
            "vue": "Vue.js",
            "@vue/cli": "Vue.js",
            "nuxt": "Nuxt.js",
            "@nuxt/core": "Nuxt.js",
            "angular": "Angular",
            "@angular/core": "Angular",
            "express": "Express.js",
            "koa": "Koa.js",
            "hapi": "Hapi.js",
            "@hapi/hapi": "Hapi.js",
            "next": "Next.js",
            "gatsby": "Gatsby",
            "svelte": "Svelte",
            "ember-cli": "Ember.js",
            "ember-source": "Ember.js",
            "meteor": "Meteor",
            "jquery": "jQuery",
            "backbone": "Backbone.js",
            "preact": "Preact",
            "nestjs": "NestJS",
            "@nestjs/core": "NestJS",
            "electron": "Electron",
        }
        
        # Check dependencies
        for dep, framework in framework_mapping.items():
            if dep in node_deps or dep in node_dev_deps:
                if framework not in frameworks:
                    frameworks.append(framework)
                    
        # Add more specialized detection for specific frameworks
        if "react" in node_deps:
            if "react-dom" in node_deps:
                # Check if it's a React web app
                if "React" in frameworks:
                    frameworks[frameworks.index("React")] = "React (Web)"
            if "react-native" in node_deps:
                # Check if it's a React Native app
                if "React" in frameworks:
                    frameworks[frameworks.index("React")] = "React (Native)"
                else:
                    frameworks.append("React (Native)")
                    
        # Detect frameworks based on file patterns
        js_files = []
        for ext in [".js", ".jsx", ".ts", ".tsx"]:
            if ext in files_by_extension:
                js_files.extend(files_by_extension[ext])
                
        if js_files:
            # Define patterns to identify frameworks from code
            framework_patterns = {
                "React": [
                    r"import\s+React",
                    r"from\s+['\"]react['\"]",
                    r"React\.Component",
                    r"extends\s+Component",
                    r"React\.createElement",
                    r"React\.render",
                ],
                "Vue.js": [
                    r"import\s+Vue",
                    r"from\s+['\"]vue['\"]",
                    r"new\s+Vue\(",
                    r"Vue\.component",
                    r"Vue\.use",
                ],
                "Angular": [
                    r"import\s+{\s*Component\s*}",
                    r"from\s+['\"]@angular/core['\"]",
                    r"@Component\(",
                    r"NgModule",
                ],
                "Express.js": [
                    r"import\s+express",
                    r"require\(['\"]express['\"]",
                    r"app\.use\(",
                    r"app\.get\(",
                    r"app\.post\(",
                ],
                "Next.js": [
                    r"import\s+{\s*AppProps\s*}",
                    r"from\s+['\"]next/app['\"]",
                    r"import\s+{\s*NextPage\s*}",
                    r"from\s+['\"]next['\"]",
                ],
                "Gatsby": [
                    r"from\s+['\"]gatsby['\"]",
                    r"graphql`",
                    r"export\s+const\s+query\s*=\s*graphql`",
                ],
                "Svelte": [
                    r"<script>",
                    r"<style>",
                    r"export\s+let\s+",
                ],
            }
            
            # Run pattern analysis
            pattern_results = self.analyze_file_patterns(js_files, framework_patterns)
            
            # Add pattern-detected frameworks to our list
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
        Detect JavaScript libraries.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected libraries
        """
        libraries = []
        
        # Check for libraries in package dependencies
        node_deps = package_deps["node"]["dependencies"]
        node_dev_deps = package_deps["node"]["devDependencies"]
        
        # Library mapping
        library_mapping = {
            "redux": "Redux",
            "@reduxjs/toolkit": "Redux Toolkit",
            "react-redux": "React Redux",
            "mobx": "MobX",
            "mobx-react": "MobX React",
            "lodash": "Lodash",
            "ramda": "Ramda",
            "axios": "Axios",
            "apollo-client": "Apollo Client",
            "@apollo/client": "Apollo Client",
            "graphql": "GraphQL",
            "d3": "D3.js",
            "three": "Three.js",
            "moment": "Moment.js",
            "dayjs": "Day.js",
            "date-fns": "date-fns",
            "luxon": "Luxon",
            "styled-components": "Styled Components",
            "emotion": "Emotion",
            "@emotion/core": "Emotion",
            "@emotion/react": "Emotion",
            "tailwindcss": "Tailwind CSS",
            "bootstrap": "Bootstrap",
            "react-bootstrap": "React Bootstrap",
            "@material-ui/core": "Material UI",
            "@mui/material": "Material UI",
            "antd": "Ant Design",
            "chakra-ui": "Chakra UI",
            "@chakra-ui/react": "Chakra UI",
            "formik": "Formik",
            "react-hook-form": "React Hook Form",
            "react-router": "React Router",
            "react-router-dom": "React Router",
            "socket.io": "Socket.IO",
            "socketio": "Socket.IO",
            "rxjs": "RxJS",
        }
        
        # Check dependencies
        for dep, library in library_mapping.items():
            if dep in node_deps or dep in node_dev_deps:
                if library not in libraries:
                    libraries.append(library)
                    
        # Detect libraries based on file patterns
        js_files = []
        for ext in [".js", ".jsx", ".ts", ".tsx"]:
            if ext in files_by_extension:
                js_files.extend(files_by_extension[ext])
                
        if js_files:
            # Define patterns to identify libraries from code
            library_patterns = {
                "Redux": [
                    r"import\s+{\s*createStore\s*}",
                    r"from\s+['\"]redux['\"]",
                    r"combineReducers",
                    r"applyMiddleware",
                ],
                "Axios": [
                    r"import\s+axios",
                    r"from\s+['\"]axios['\"]",
                    r"axios\.get\(",
                    r"axios\.post\(",
                ],
                "GraphQL": [
                    r"import\s+{\s*gql\s*}",
                    r"from\s+['\"]graphql-tag['\"]",
                    r"import\s+gql",
                    r"from\s+['\"]@apollo/client['\"]",
                ],
                "Lodash": [
                    r"import\s+_",
                    r"from\s+['\"]lodash['\"]",
                    r"import\s+{\s*map\s*}",
                    r"from\s+['\"]lodash['\"]",
                ],
                "Socket.IO": [
                    r"import\s+io",
                    r"from\s+['\"]socket\.io-client['\"]",
                    r"io\(['\"]",
                    r"socket\.on\(",
                ],
            }
            
            # Run pattern analysis
            pattern_results = self.analyze_file_patterns(js_files, library_patterns)
            
            # Add pattern-detected libraries to our list
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
        Detect JavaScript tools.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected tools
        """
        tools = []
        
        # Check for tools in package dependencies
        node_deps = package_deps["node"]["dependencies"]
        node_dev_deps = package_deps["node"]["devDependencies"]
        
        # Tool mapping
        tool_mapping = {
            "webpack": "Webpack",
            "vite": "Vite",
            "parcel": "Parcel",
            "rollup": "Rollup",
            "babel": "Babel",
            "@babel/core": "Babel",
            "typescript": "TypeScript",
            "eslint": "ESLint",
            "prettier": "Prettier",
            "jest": "Jest",
            "ts-jest": "Jest",
            "mocha": "Mocha",
            "chai": "Chai",
            "cypress": "Cypress",
            "selenium-webdriver": "Selenium",
            "puppeteer": "Puppeteer",
            "playwright": "Playwright",
            "storybook": "Storybook",
            "@storybook/react": "Storybook",
            "@storybook/vue": "Storybook",
            "lerna": "Lerna",
            "nx": "Nx",
            "gulp": "Gulp",
            "grunt": "Grunt",
        }
        
        # Check dependencies
        for dep, tool in tool_mapping.items():
            if dep in node_deps or dep in node_dev_deps:
                if tool not in tools:
                    tools.append(tool)
                    
        # Check for configuration files that indicate tool usage
        config_files = {
            "webpack.config.js": "Webpack",
            ".babelrc": "Babel",
            "babel.config.js": "Babel",
            "tsconfig.json": "TypeScript",
            ".eslintrc": "ESLint",
            ".eslintrc.js": "ESLint",
            ".eslintrc.json": "ESLint",
            ".prettierrc": "Prettier",
            ".prettierrc.js": "Prettier",
            "jest.config.js": "Jest",
            "cypress.json": "Cypress",
            "cypress.config.js": "Cypress",
            ".storybook": "Storybook",
            "lerna.json": "Lerna",
            "nx.json": "Nx",
            "gulpfile.js": "Gulp",
            "Gruntfile.js": "Grunt",
            "vite.config.js": "Vite",
            "rollup.config.js": "Rollup",
        }
        
        for config_file, tool in config_files.items():
            if (self.base_path / config_file).exists() or (self.base_path / config_file).is_dir():
                if tool not in tools:
                    tools.append(tool)
                    
        return tools 