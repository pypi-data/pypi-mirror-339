"""
Python framework detector.

This module provides a detector for Python frameworks and libraries.
"""

from pathlib import Path
from typing import Dict, List, Any

from amauta_ai.analyzer.framework_detection.base import FrameworkDetector
from amauta_ai.analyzer.framework_detection.registry import register


@register
class PythonFrameworkDetector(FrameworkDetector):
    """
    Detector for Python frameworks and libraries.
    
    This detector identifies Python frameworks, libraries,
    and tools based on package dependencies and code patterns.
    """
    
    @property
    def language(self) -> str:
        """
        Get the language this detector handles.
        
        Returns:
            The name of the language this detector handles
        """
        return "Python"
        
    def is_language_present(self, files_by_extension: Dict[str, List[Path]]) -> bool:
        """
        Check if Python is present in the codebase.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            
        Returns:
            True if Python is present, False otherwise
        """
        return ".py" in files_by_extension
        
    def detect_frameworks(
        self,
        files_by_extension: Dict[str, List[Path]],
        package_deps: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """
        Detect Python frameworks.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected frameworks
        """
        frameworks = []
        
        # Check for frameworks in package dependencies
        python_deps = package_deps["python"]["dependencies"]
        python_dev_deps = package_deps["python"]["devDependencies"]
        
        # Framework detection based on package dependencies
        framework_mapping = {
            "django": "Django",
            "flask": "Flask",
            "fastapi": "FastAPI",
            "tornado": "Tornado",
            "pyramid": "Pyramid",
            "bottle": "Bottle",
            "cherrypy": "CherryPy",
            "falcon": "Falcon",
            "starlette": "Starlette",
            "sanic": "Sanic",
            "quart": "Quart",
            "responder": "Responder",
            "dash": "Dash",
            "streamlit": "Streamlit",
            "gradio": "Gradio",
            "scrapy": "Scrapy",
            "celery": "Celery",
            "airflow": "Airflow",
            "luigi": "Luigi",
            "kafka": "Kafka Python",
            "faust": "Faust",
            "ray": "Ray",
            "pyspark": "PySpark",
            "dask": "Dask",
            "dagster": "Dagster",
            "kedro": "Kedro",
        }
        
        # Check dependencies
        for dep, framework in framework_mapping.items():
            if dep in python_deps or dep in python_dev_deps:
                if framework not in frameworks:
                    frameworks.append(framework)
                    
        # Check for required files that indicate framework usage
        if (self.base_path / "manage.py").exists():
            if "Django" not in frameworks:
                frameworks.append("Django")
                
        if (self.base_path / "app.py").exists() or (self.base_path / "wsgi.py").exists():
            # Check the content of app.py to distinguish between Flask and other frameworks
            try:
                app_py_path = self.base_path / "app.py"
                if app_py_path.exists():
                    with open(app_py_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if "Flask" in content and "Flask" not in frameworks:
                            frameworks.append("Flask")
                        elif "FastAPI" in content and "FastAPI" not in frameworks:
                            frameworks.append("FastAPI")
            except Exception:
                pass
                
        # Detect frameworks based on file patterns
        py_files = files_by_extension.get(".py", [])
        
        if py_files:
            # Define patterns to identify frameworks from code
            framework_patterns = {
                "Django": [
                    r"from\s+django",
                    r"django\.db",
                    r"django\.http",
                    r"django\.shortcuts",
                    r"django\.views",
                    r"django\.contrib",
                    r"django\.urls",
                ],
                "Flask": [
                    r"from\s+flask\s+import",
                    r"Flask\(",
                    r"@app\.route",
                ],
                "FastAPI": [
                    r"from\s+fastapi\s+import",
                    r"FastAPI\(",
                    r"@app\.get",
                    r"@app\.post",
                ],
                "Tornado": [
                    r"import\s+tornado",
                    r"from\s+tornado",
                    r"tornado\.web",
                    r"class.*\(tornado\.web\.RequestHandler\)",
                ],
                "Pyramid": [
                    r"from\s+pyramid",
                    r"config\.add_route",
                    r"config\.add_view",
                ],
                "Bottle": [
                    r"from\s+bottle\s+import",
                    r"@route\(",
                    r"@get\(",
                    r"@post\(",
                ],
                "Scrapy": [
                    r"import\s+scrapy",
                    r"from\s+scrapy",
                    r"class.*\(scrapy\.Spider\)",
                ],
                "Celery": [
                    r"from\s+celery\s+import",
                    r"@app\.task",
                    r"@shared_task",
                ],
                "Airflow": [
                    r"from\s+airflow",
                    r"DAG\(",
                    r"@task",
                ],
                "Streamlit": [
                    r"import\s+streamlit\s+as\s+st",
                    r"st\.(title|header|sidebar|checkbox|button|selectbox)",
                ],
                "Dash": [
                    r"import\s+dash",
                    r"from\s+dash",
                    r"dash\.Dash",
                    r"app\.layout",
                ],
            }
            
            # Run pattern analysis
            pattern_results = self.analyze_file_patterns(py_files, framework_patterns)
            
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
        Detect Python libraries.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected libraries
        """
        libraries = []
        
        # Check for libraries in package dependencies
        python_deps = package_deps["python"]["dependencies"]
        python_dev_deps = package_deps["python"]["devDependencies"]
        
        # Library mapping
        library_mapping = {
            "numpy": "NumPy",
            "scipy": "SciPy",
            "pandas": "Pandas",
            "matplotlib": "Matplotlib",
            "seaborn": "Seaborn",
            "plotly": "Plotly",
            "bokeh": "Bokeh",
            "scikit-learn": "Scikit-learn",
            "sklearn": "Scikit-learn",
            "tensorflow": "TensorFlow",
            "torch": "PyTorch",
            "keras": "Keras",
            "transformers": "Transformers",
            "huggingface-hub": "Hugging Face Hub",
            "spacy": "spaCy",
            "nltk": "NLTK",
            "gensim": "Gensim",
            "networkx": "NetworkX",
            "requests": "Requests",
            "httpx": "HTTPX",
            "aiohttp": "AIOHTTP",
            "beautifulsoup4": "BeautifulSoup",
            "bs4": "BeautifulSoup",
            "sqlalchemy": "SQLAlchemy",
            "alembic": "Alembic",
            "pydantic": "Pydantic",
            "marshmallow": "Marshmallow",
            "dataclasses-json": "dataclasses-json",
            "langchain": "LangChain",
            "llama-index": "LlamaIndex",
            "openai": "OpenAI API",
            "anthropic": "Anthropic API",
            "pytest": "pytest",
            "unittest": "unittest",
            "pytest-cov": "pytest-cov",
            "coverage": "coverage",
            "pillow": "Pillow",
            "opencv-python": "OpenCV",
            "click": "Click",
            "typer": "Typer",
            "rich": "Rich",
            "tqdm": "tqdm",
            "jinja2": "Jinja2",
            "jinja": "Jinja2",
            "pymongo": "PyMongo",
            "redis": "Redis",
            "psycopg2": "psycopg2",
            "psycopg2-binary": "psycopg2",
            "asyncpg": "asyncpg",
            "websockets": "websockets",
            "uvicorn": "Uvicorn",
            "gunicorn": "Gunicorn",
        }
        
        # Check dependencies
        for dep, library in library_mapping.items():
            if dep in python_deps or dep in python_dev_deps:
                if library not in libraries:
                    libraries.append(library)
                    
        # Detect libraries based on file patterns
        py_files = files_by_extension.get(".py", [])
        
        if py_files:
            # Define patterns to identify libraries from code
            library_patterns = {
                "NumPy": [
                    r"import\s+numpy",
                    r"from\s+numpy",
                    r"np\.(array|ndarray|zeros|ones|random)",
                ],
                "Pandas": [
                    r"import\s+pandas",
                    r"from\s+pandas",
                    r"pd\.(DataFrame|Series|read_csv|read_excel)",
                ],
                "Matplotlib": [
                    r"import\s+matplotlib",
                    r"from\s+matplotlib",
                    r"plt\.(figure|plot|scatter|bar|hist)",
                ],
                "Requests": [
                    r"import\s+requests",
                    r"requests\.(get|post|put|delete)",
                ],
                "SQLAlchemy": [
                    r"import\s+sqlalchemy",
                    r"from\s+sqlalchemy",
                    r"db\.(Column|String|Integer|Boolean|relationship)",
                ],
                "Pydantic": [
                    r"from\s+pydantic\s+import",
                    r"class.*\(BaseModel\)",
                ],
                "LangChain": [
                    r"from\s+langchain",
                    r"langchain\.(llms|chains|embeddings|agents|tools)",
                ],
                "Typer": [
                    r"import\s+typer",
                    r"from\s+typer",
                    r"typer\.Typer\(",
                ],
                "Rich": [
                    r"from\s+rich",
                    r"rich\.(print|console|panel|table)",
                ],
            }
            
            # Run pattern analysis
            pattern_results = self.analyze_file_patterns(py_files, library_patterns)
            
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
        Detect Python tools.
        
        Args:
            files_by_extension: Dictionary mapping file extensions to lists of file paths
            package_deps: Dictionary containing package dependency information
            
        Returns:
            List of detected tools
        """
        tools = []
        
        # Check for tools in package dependencies
        python_deps = package_deps["python"]["dependencies"]
        python_dev_deps = package_deps["python"]["devDependencies"]
        
        # Tool mapping
        tool_mapping = {
            "black": "Black",
            "isort": "isort",
            "flake8": "Flake8",
            "pylint": "Pylint",
            "mypy": "MyPy",
            "pyre-check": "Pyre",
            "pyright": "Pyright",
            "bandit": "Bandit",
            "safety": "Safety",
            "ruff": "Ruff",
            "poetry": "Poetry",
            "pipenv": "Pipenv",
            "pip-tools": "pip-tools",
            "setuptools": "setuptools",
            "wheel": "wheel",
            "twine": "twine",
            "sphinx": "Sphinx",
            "mkdocs": "MkDocs",
            "jupyter": "Jupyter",
            "ipython": "IPython",
            "pre-commit": "pre-commit",
            "tox": "tox",
            "nox": "nox",
            "docker-compose": "Docker Compose",
        }
        
        # Check dependencies
        for dep, tool in tool_mapping.items():
            if dep in python_deps or dep in python_dev_deps:
                if tool not in tools:
                    tools.append(tool)
                    
        # Check for configuration files that indicate tool usage
        config_files = {
            ".flake8": "Flake8",
            "setup.cfg": "setuptools",
            "setup.py": "setuptools",
            "pyproject.toml": "Modern Python packaging",
            "poetry.lock": "Poetry",
            "Pipfile": "Pipenv",
            "Pipfile.lock": "Pipenv",
            "requirements.txt": "pip",
            "dev-requirements.txt": "pip",
            "requirements-dev.txt": "pip",
            "mypy.ini": "MyPy",
            "tox.ini": "tox",
            ".pre-commit-config.yaml": "pre-commit",
            "conftest.py": "pytest",
            "pytest.ini": "pytest",
            "Dockerfile": "Docker",
            "docker-compose.yml": "Docker Compose",
            "docker-compose.yaml": "Docker Compose",
            ".github/workflows": "GitHub Actions",
            ".gitlab-ci.yml": "GitLab CI",
        }
        
        for config_file, tool in config_files.items():
            if (self.base_path / config_file).exists() or (self.base_path / config_file).is_dir():
                if tool not in tools:
                    tools.append(tool)
                    
        # Special case for pyproject.toml - check its content to determine tools
        pyproject_path = self.base_path / "pyproject.toml"
        if pyproject_path.exists():
            try:
                with open(pyproject_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "[tool.poetry]" in content and "Poetry" not in tools:
                        tools.append("Poetry")
                    if "[tool.black]" in content and "Black" not in tools:
                        tools.append("Black")
                    if "[tool.isort]" in content and "isort" not in tools:
                        tools.append("isort")
                    if "[tool.ruff]" in content and "Ruff" not in tools:
                        tools.append("Ruff")
                    if "[tool.mypy]" in content and "MyPy" not in tools:
                        tools.append("MyPy")
            except Exception:
                pass
                
        return tools 