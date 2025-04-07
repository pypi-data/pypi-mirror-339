"""
Test configuration utilities for LightWave projects.

This module provides tools to configure pytest for different project types.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

# Try importing toml, fall back to using tomli
try:
    import toml
except ImportError:
    try:
        import tomli as toml
    except ImportError:
        # For Python 3.11+ we can use tomllib
        try:
            import tomllib as toml
        except ImportError:
            # If no TOML library is available, define a minimal parser
            toml = None
            print("WARNING: No TOML library available. Limited functionality.")

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

console = Console()

def configure_pytest(
    directory: str = ".",
    framework: Optional[str] = None,
    create_example_tests: bool = False,
    plugins: List[str] = None,
    markers: List[str] = None,
    interactive: bool = True,
) -> bool:
    """
    Configure pytest for a project.
    
    Args:
        directory: Project root directory
        framework: Web framework (django, flask, fastapi)
        create_example_tests: Create example test files
        plugins: Pytest plugins to configure
        markers: Custom pytest markers to add
        interactive: Enable interactive configuration
        
    Returns:
        True if configuration was successful
    """
    from .runner import detect_project_type
    
    base_path = Path(directory).absolute()
    
    # Detect project type if not specified
    if not framework or not plugins:
        project_info = detect_project_type(directory)
        if not framework:
            framework = project_info["framework"]
        
        if not plugins and "plugins" in project_info["suggested_settings"]:
            suggested_plugins = project_info["suggested_settings"].get("plugins", [])
            if not plugins:
                plugins = []
            for plugin in suggested_plugins:
                if plugin not in plugins:
                    plugins.append(plugin)
    
    # Define standard markers if none provided
    if not markers:
        markers = [
            "unit: marks tests as unit tests",
            "integration: marks tests as integration tests",
            "e2e: marks tests as end-to-end tests",
        ]
        
        if framework == "django":
            markers.extend([
                "django: marks tests that require django",
                "urls: marks tests for URL routing",
                "models: marks tests for Django models",
                "views: marks tests for Django views",
                "forms: marks tests for Django forms",
            ])
        elif framework == "fastapi":
            markers.extend([
                "api: marks tests for API endpoints",
                "routes: marks tests for route handling",
                "async: marks async tests",
            ])
        elif framework == "flask":
            markers.extend([
                "routes: marks tests for Flask routes",
                "blueprints: marks tests for Flask blueprints",
                "extensions: marks tests for Flask extensions",
            ])
    
    # Interactive mode
    if interactive:
        console.print("[bold]Pytest Configuration Wizard[/bold]")
        
        if framework:
            console.print(f"Detected framework: [bold]{framework}[/bold]")
        else:
            frameworks = ["django", "flask", "fastapi", "none"]
            framework = Prompt.ask(
                "Select framework",
                choices=frameworks,
                default="none"
            )
        
        # Ask about plugins
        default_plugins = {
            "django": ["pytest-django"],
            "flask": ["pytest-flask"],
            "fastapi": ["pytest-asyncio"],
        }
        
        if not plugins:
            plugins = []
            
            if framework in default_plugins:
                for plugin in default_plugins[framework]:
                    if Confirm.ask(f"Add {plugin}?", default=True):
                        plugins.append(plugin)
        
        # Common plugins to offer
        common_plugins = [
            "pytest-cov",
            "pytest-xdist",
            "pytest-mock",
            "pytest-html",
            "pytest-timeout",
        ]
        
        for plugin in common_plugins:
            if plugin not in plugins and Confirm.ask(f"Add {plugin}?", default=True):
                plugins.append(plugin)
        
        # Ask about example tests
        create_example_tests = Confirm.ask("Create example tests?", default=True)
    
    # Create tests directory if it doesn't exist
    tests_dir = base_path / "tests"
    if not tests_dir.exists():
        tests_dir.mkdir(parents=True)
        console.print(f"[green]Created tests directory: {tests_dir}[/green]")
    
    # Create conftest.py with basic fixtures
    conftest_path = tests_dir / "conftest.py"
    if not conftest_path.exists() or Confirm.ask("Overwrite existing conftest.py?", default=False):
        create_conftest_py(conftest_path, framework)
        console.print(f"[green]Created conftest.py: {conftest_path}[/green]")
    
    # Update pyproject.toml
    pyproject_path = base_path / "pyproject.toml"
    if pyproject_path.exists():
        update_pyproject_toml(pyproject_path, markers, plugins)
        console.print(f"[green]Updated pytest configuration in pyproject.toml[/green]")
    else:
        # Create pytest.ini if pyproject.toml doesn't exist
        pytest_ini_path = base_path / "pytest.ini"
        create_pytest_ini(pytest_ini_path, markers, plugins)
        console.print(f"[green]Created pytest.ini: {pytest_ini_path}[/green]")
    
    # Create example tests if requested
    if create_example_tests:
        create_example_test_files(tests_dir, framework)
        console.print(f"[green]Created example test files in: {tests_dir}[/green]")
    
    # Show summary
    console.print("\n[bold]Configuration Summary[/bold]")
    table = Table()
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Framework", framework or "Not specified")
    table.add_row("Plugins", ", ".join(plugins or []))
    table.add_row("Example Tests", "Yes" if create_example_tests else "No")
    
    console.print(table)
    console.print("\n[bold green]Pytest configuration complete![/bold green]")
    console.print("Run tests with: [bold]lightwave test run[/bold]")
    
    return True

def create_conftest_py(path: Path, framework: Optional[str] = None) -> None:
    """Create a conftest.py file with framework-specific fixtures."""
    content = """\"\"\"
Pytest configuration for project.

This file contains fixtures and configuration for tests.
\"\"\"

import pytest
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).parent.parent

@pytest.fixture
def base_dir():
    \"\"\"Return the base directory of the project.\"\"\"
    return BASE_DIR

"""
    
    # Add framework-specific fixtures
    if framework == "django":
        content += """
# Django fixtures
@pytest.fixture
def api_client():
    \"\"\"Return a Django REST framework API client.\"\"\"
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def authenticated_client(db, django_user_model):
    \"\"\"Return an authenticated client.\"\"\"
    from django.test import Client
    
    username = "testuser"
    password = "testpassword"
    
    django_user_model.objects.create_user(username=username, password=password)
    client = Client()
    client.login(username=username, password=password)
    
    return client
"""
    elif framework == "fastapi":
        content += """
# FastAPI fixtures
@pytest.fixture
def app():
    \"\"\"Create a FastAPI test application.\"\"\"
    from fastapi.testclient import TestClient
    # Import your FastAPI app
    # from app.main import app
    # For this example, we'll create a simple test app
    from fastapi import FastAPI
    
    app = FastAPI()
    
    @app.get("/test")
    def read_test():
        return {"message": "Test endpoint"}
    
    return app

@pytest.fixture
def client(app):
    \"\"\"Return a FastAPI test client.\"\"\"
    from fastapi.testclient import TestClient
    return TestClient(app)
"""
    elif framework == "flask":
        content += """
# Flask fixtures
@pytest.fixture
def app():
    \"\"\"Create a Flask test application.\"\"\"
    # Import your Flask app or create a test instance
    # from app import create_app
    # For this example, we'll create a simple test app
    from flask import Flask
    
    app = Flask(__name__)
    app.config.update({
        "TESTING": True,
    })
    
    @app.route("/test")
    def test():
        return "Test endpoint"
    
    return app

@pytest.fixture
def client(app):
    \"\"\"Return a Flask test client.\"\"\"
    return app.test_client()
"""
    
    # Write conftest.py
    with open(path, "w") as f:
        f.write(content)

def update_pyproject_toml(path: Path, markers: List[str], plugins: List[str] = None) -> None:
    """Update pytest configuration in pyproject.toml."""
    try:
        # Read existing content
        with open(path, "r") as f:
            config = toml.load(f)
        
        # Create tool.pytest section if it doesn't exist
        if "tool" not in config:
            config["tool"] = {}
        if "pytest" not in config["tool"]:
            config["tool"]["pytest"] = {}
        if "ini_options" not in config["tool"]["pytest"]:
            config["tool"]["pytest"]["ini_options"] = {}
        
        # Set pytest options
        pytest_config = config["tool"]["pytest"]["ini_options"]
        
        # Basic configuration
        pytest_config["testpaths"] = ["tests"]
        pytest_config["python_files"] = "test_*.py"
        pytest_config["python_classes"] = "Test*"
        pytest_config["python_functions"] = "test_*"
        
        # Add markers
        if markers:
            pytest_config["markers"] = markers
        
        # Add addopts if plugins specified
        if plugins:
            addopts = []
            for plugin in plugins:
                if plugin == "pytest-cov":
                    addopts.append("--cov")
                if plugin == "pytest-xdist":
                    addopts.append("-n auto")
                if plugin == "pytest-html":
                    addopts.append("--html=report.html")
                    addopts.append("--self-contained-html")
            
            if addopts:
                pytest_config["addopts"] = " ".join(addopts)
        
        # Write updated configuration
        with open(path, "w") as f:
            toml.dump(config, f)
    
    except Exception as e:
        console.print(f"[bold red]Error updating pyproject.toml: {str(e)}[/bold red]")

def create_pytest_ini(path: Path, markers: List[str], plugins: List[str] = None) -> None:
    """Create a pytest.ini file."""
    content = """[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
"""
    
    # Add markers
    if markers:
        content += "\nmarkers =\n"
        for marker in markers:
            content += f"    {marker}\n"
    
    # Add addopts if plugins specified
    if plugins:
        addopts = []
        for plugin in plugins:
            if plugin == "pytest-cov":
                addopts.append("--cov")
            if plugin == "pytest-xdist":
                addopts.append("-n auto")
            if plugin == "pytest-html":
                addopts.append("--html=report.html")
                addopts.append("--self-contained-html")
        
        if addopts:
            content += "\naddopts = " + " ".join(addopts) + "\n"
    
    # Write pytest.ini
    with open(path, "w") as f:
        f.write(content)

def create_example_test_files(tests_dir: Path, framework: Optional[str] = None) -> None:
    """Create example test files based on framework."""
    # Create test_basic.py
    basic_test_path = tests_dir / "test_basic.py"
    with open(basic_test_path, "w") as f:
        f.write("""\"\"\"
Basic tests for the project.
\"\"\"

import pytest

def test_truth():
    \"\"\"Test that True is true.\"\"\"
    assert True

def test_math():
    \"\"\"Test basic math.\"\"\"
    assert 2 + 2 == 4

@pytest.mark.unit
def test_unit_example():
    \"\"\"Example unit test.\"\"\"
    value = "test"
    assert value == "test"

@pytest.mark.parametrize("input_val,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input_val, expected):
    \"\"\"Test squaring numbers with parametrize.\"\"\"
    assert input_val * input_val == expected
""")
    
    # Framework-specific test examples
    if framework == "django":
        django_test_path = tests_dir / "test_django.py"
        with open(django_test_path, "w") as f:
            f.write("""\"\"\"
Django test examples.
\"\"\"

import pytest

@pytest.mark.django_db
def test_db_access():
    \"\"\"Test database access.\"\"\"
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    count = User.objects.count()
    assert count >= 0

@pytest.mark.django_db
@pytest.mark.models
def test_create_user(django_user_model):
    \"\"\"Test creating a Django user.\"\"\"
    username = "testuser"
    email = "test@example.com"
    password = "testpass123"
    
    user = django_user_model.objects.create_user(
        username=username,
        email=email,
        password=password,
    )
    
    assert user.username == username
    assert user.email == email
    assert user.check_password(password)

@pytest.mark.urls
def test_admin_url(client):
    \"\"\"Test that admin URL returns correct status code.\"\"\"
    response = client.get("/admin/")
    assert response.status_code == 302  # Redirect to login
    
@pytest.mark.views
def test_authenticated_view(authenticated_client):
    \"\"\"Test an authenticated view.\"\"\"
    # Example assumes you have a protected view at /profile/
    response = authenticated_client.get("/admin/")
    assert response.status_code == 200
""")
    
    elif framework == "fastapi":
        fastapi_test_path = tests_dir / "test_fastapi.py"
        with open(fastapi_test_path, "w") as f:
            f.write("""\"\"\"
FastAPI test examples.
\"\"\"

import pytest
from fastapi.testclient import TestClient

@pytest.mark.api
def test_api_endpoint(client):
    \"\"\"Test a FastAPI endpoint.\"\"\"
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json() == {"message": "Test endpoint"}

@pytest.mark.async
async def test_async_endpoint(app):
    \"\"\"Test an async endpoint.\"\"\"
    # Create a test async endpoint
    @app.get("/async-test")
    async def read_async_test():
        return {"message": "Async test endpoint"}
    
    # Test with sync TestClient
    client = TestClient(app)
    response = client.get("/async-test")
    assert response.status_code == 200
    assert response.json() == {"message": "Async test endpoint"}

@pytest.mark.api
def test_post_request(client):
    \"\"\"Test a POST request.\"\"\"
    # Add a test POST endpoint to the app
    from fastapi import FastAPI
    app.post("/post-test")
    
    response = client.post(
        "/post-test",
        json={"key": "value"}
    )
    assert response.status_code in (200, 422)  # Depends on validation
""")
    
    elif framework == "flask":
        flask_test_path = tests_dir / "test_flask.py"
        with open(flask_test_path, "w") as f:
            f.write("""\"\"\"
Flask test examples.
\"\"\"

import pytest

@pytest.mark.routes
def test_route(client):
    \"\"\"Test a Flask route.\"\"\"
    response = client.get("/test")
    assert response.status_code == 200
    assert response.data == b"Test endpoint"

@pytest.mark.parametrize("route", [
    "/test",
    "/missing",
])
def test_multiple_routes(client, route):
    \"\"\"Test multiple routes.\"\"\"
    response = client.get(route)
    if route == "/test":
        assert response.status_code == 200
    else:
        assert response.status_code == 404

def test_app_config(app):
    \"\"\"Test the Flask app configuration.\"\"\"
    assert app.config["TESTING"] is True
""") 