"""
Test runner for LightWave projects.

This module provides a centralized way to run pytest tests with various configurations.
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Union, Any
import json
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def run_tests(
    test_paths: List[str] = None,
    markers: List[str] = None,
    keywords: List[str] = None,
    verbose: bool = False,
    coverage: bool = False,
    coverage_report: str = "term",
    parallel: bool = False,
    num_processes: int = None,
    config_file: Optional[str] = None,
    env_vars: Dict[str, str] = None,
    timeout: Optional[int] = None,
    html_report: Optional[str] = None,
    junit_report: Optional[str] = None,
    collect_only: bool = False,
    failfast: bool = False,
    framework: str = None,
    plugins: List[str] = None,
    project_type: str = None,
    settings_module: Optional[str] = None,
    extra_args: List[str] = None,
) -> int:
    """
    Run tests using pytest with the specified configuration.
    
    Args:
        test_paths: Paths to test files or directories
        markers: Pytest markers to select tests
        keywords: Keywords to filter tests
        verbose: Enable verbose output
        coverage: Enable code coverage
        coverage_report: Coverage report type (term, html, xml)
        parallel: Run tests in parallel using pytest-xdist
        num_processes: Number of processes for parallel testing
        config_file: Path to pytest config file
        env_vars: Environment variables to set
        timeout: Test timeout in seconds
        html_report: Path for HTML report
        junit_report: Path for JUnit XML report
        collect_only: Only collect tests, don't run them
        failfast: Stop on first failure
        framework: Web framework (django, flask, fastapi)
        plugins: Additional pytest plugins to use
        project_type: Type of project (web, cli, api, etc.)
        settings_module: Django settings module
        extra_args: Additional pytest command line arguments
        
    Returns:
        Exit code from pytest
    """
    pytest_args = []
    
    # Add test paths
    if test_paths:
        pytest_args.extend(test_paths)
    else:
        pytest_args.append("tests/")
    
    # Add markers
    if markers:
        for marker in markers:
            pytest_args.append(f"-m {marker}")
    
    # Add keywords
    if keywords:
        for keyword in keywords:
            pytest_args.append(f"-k {keyword}")
    
    # Verbose mode
    if verbose:
        pytest_args.append("-v")
        
    # Fail fast
    if failfast:
        pytest_args.append("--exitfirst")
    
    # Collection only
    if collect_only:
        pytest_args.append("--collect-only")
    
    # Coverage options
    if coverage:
        pytest_args.append("--cov")
        
        if coverage_report:
            report_types = coverage_report.split(",")
            for report_type in report_types:
                pytest_args.append(f"--cov-report={report_type.strip()}")
    
    # HTML report
    if html_report:
        pytest_args.append(f"--html={html_report}")
        pytest_args.append("--self-contained-html")
    
    # JUnit XML report
    if junit_report:
        pytest_args.append(f"--junitxml={junit_report}")
    
    # Parallel execution
    if parallel:
        if num_processes:
            pytest_args.append(f"-n {num_processes}")
        else:
            pytest_args.append("-n auto")
    
    # Config file
    if config_file:
        pytest_args.append(f"-c {config_file}")
    
    # Timeout
    if timeout:
        pytest_args.append(f"--timeout={timeout}")
    
    # Framework-specific settings
    if framework:
        if framework.lower() == "django":
            pytest_args.append("--ds=" + (settings_module or "config.settings.test"))
            
        elif framework.lower() == "fastapi":
            # Add specific FastAPI testing options if needed
            pass
            
        elif framework.lower() == "flask":
            # Add specific Flask testing options if needed
            pass
    
    # Add extra arguments
    if extra_args:
        pytest_args.extend(extra_args)
    
    # Build the command
    cmd = ["python", "-m", "pytest"] + pytest_args
    
    # Set environment variables
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)
    
    # Display command
    console.print(f"[bold blue]Running: {' '.join(cmd)}[/bold blue]")
    
    # Run tests with progress indicator
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Running tests...[/bold blue]"),
        console=console,
        transient=True,
    ) as progress:
        progress.add_task("run", total=None)
        
        try:
            result = subprocess.run(
                cmd,
                env=env,
                check=False,
                text=True,
            )
            return result.returncode
        except Exception as e:
            console.print(f"[bold red]Error running tests: {str(e)}[/bold red]")
            return 1

def detect_project_type(directory: str = ".") -> Dict[str, Any]:
    """
    Detect the type of project based on files and directories present.
    
    Args:
        directory: Base directory to check
        
    Returns:
        Dictionary with detected project info
    """
    base_path = Path(directory).absolute()
    
    project_info = {
        "framework": None,
        "is_django": False,
        "is_flask": False,
        "is_fastapi": False,
        "is_cli": False,
        "has_pytest_config": False,
        "suggested_settings": {},
    }
    
    # Check for framework-specific files
    if (base_path / "manage.py").exists():
        project_info["framework"] = "django"
        project_info["is_django"] = True
    
    # Check for Flask
    if list(base_path.glob("**/flask_app.py")) or list(base_path.glob("**/app.py")):
        if not project_info["framework"]:
            project_info["framework"] = "flask"
        project_info["is_flask"] = True
    
    # Check for FastAPI
    if list(base_path.glob("**/main.py")) or list(base_path.glob("**/app.py")):
        # Look for FastAPI imports
        for file in base_path.glob("**/*.py"):
            try:
                with open(file, "r") as f:
                    content = f.read()
                    if "from fastapi import" in content:
                        project_info["is_fastapi"] = True
                        if not project_info["framework"]:
                            project_info["framework"] = "fastapi"
                        break
            except Exception:
                continue
    
    # Check for CLI tools
    if list(base_path.glob("**/cli.py")) or (base_path / "pyproject.toml").exists():
        project_info["is_cli"] = True
        if not project_info["framework"]:
            project_info["framework"] = "cli"
            
            # Check for entry points in pyproject.toml
            if (base_path / "pyproject.toml").exists():
                try:
                    with open(base_path / "pyproject.toml", "r") as f:
                        content = f.read()
                        if "[project.scripts]" in content or "[console_scripts]" in content:
                            project_info["is_cli"] = True
                except Exception:
                    pass
    
    # Check for pytest configuration
    pytest_configs = [
        base_path / "pytest.ini",
        base_path / "pyproject.toml",  # Check for [tool.pytest]
        base_path / "conftest.py",
    ]
    
    for config in pytest_configs:
        if config.exists():
            project_info["has_pytest_config"] = True
            break
    
    # Set suggested settings based on project type
    if project_info["is_django"]:
        project_info["suggested_settings"] = {
            "plugins": ["pytest-django"],
            "settings_module": _find_django_settings(base_path),
        }
    elif project_info["is_flask"]:
        project_info["suggested_settings"] = {
            "plugins": ["pytest-flask"],
        }
    elif project_info["is_fastapi"]:
        project_info["suggested_settings"] = {
            "plugins": ["pytest-asyncio"],
        }
    
    return project_info

def _find_django_settings(base_path: Path) -> Optional[str]:
    """Find Django settings module path."""
    # Common Django settings paths
    settings_paths = [
        "settings.py",
        "config/settings.py",
        "project/settings.py",
        "app/settings.py",
    ]
    
    for path in settings_paths:
        if (base_path / path).exists():
            path_parts = path.split("/")
            module_path = ".".join([p.replace(".py", "") for p in path_parts])
            return module_path
    
    return None 