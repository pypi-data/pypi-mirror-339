"""
CLI interface for the testing module.

This module provides Typer commands for test operations.
"""

import os
import sys
from pathlib import Path
from typing import List, Optional
import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt

from .runner import run_tests, detect_project_type
from .configurator import configure_pytest

console = Console()
app = typer.Typer(help="Test management commands")

@app.command("run")
def run(
    test_paths: List[str] = typer.Argument(
        None, help="Paths to test files or directories"
    ),
    markers: List[str] = typer.Option(
        None, "--marker", "-m", help="Select tests with specific pytest markers"
    ),
    keywords: List[str] = typer.Option(
        None, "--keyword", "-k", help="Select tests by keyword expressions"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
    coverage: bool = typer.Option(
        False, "--coverage", "-c", help="Enable code coverage"
    ),
    coverage_report: str = typer.Option(
        "term", "--cov-report", help="Coverage report format (term, html, xml, annotate)"
    ),
    parallel: bool = typer.Option(
        False, "--parallel", "-p", help="Run tests in parallel"
    ),
    processes: Optional[int] = typer.Option(
        None, "--processes", "-n", help="Number of processes for parallel testing"
    ),
    timeout: Optional[int] = typer.Option(
        None, "--timeout", "-t", help="Test timeout in seconds"
    ),
    html_report: Optional[Path] = typer.Option(
        None, "--html", help="Generate HTML report"
    ),
    junit_report: Optional[Path] = typer.Option(
        None, "--junit", help="Generate JUnit XML report"
    ),
    config: Optional[Path] = typer.Option(
        None, "--config", "-c", help="Path to pytest config file"
    ),
    failfast: bool = typer.Option(
        False, "--failfast", "-x", help="Stop on first failure"
    ),
    collect_only: bool = typer.Option(
        False, "--collect-only", help="Only collect tests, don't run them"
    ),
    framework: Optional[str] = typer.Option(
        None, "--framework", help="Project framework (django, flask, fastapi)"
    ),
    django_settings: Optional[str] = typer.Option(
        None, "--ds", help="Django settings module"
    ),
    extra_args: List[str] = typer.Option(
        None, "--extra", help="Additional pytest arguments"
    ),
):
    """Run tests with pytest."""
    # Convert Path objects to strings
    config_file = str(config) if config else None
    html_report_path = str(html_report) if html_report else None
    junit_report_path = str(junit_report) if junit_report else None
    
    # Detect project type if framework not specified
    if not framework:
        project_info = detect_project_type()
        framework = project_info.get("framework")
    
    # Set environment variables
    env_vars = {}
    if django_settings:
        env_vars["DJANGO_SETTINGS_MODULE"] = django_settings
    
    # Run tests
    result = run_tests(
        test_paths=test_paths,
        markers=markers,
        keywords=keywords,
        verbose=verbose,
        coverage=coverage,
        coverage_report=coverage_report,
        parallel=parallel,
        num_processes=processes,
        config_file=config_file,
        env_vars=env_vars,
        timeout=timeout,
        html_report=html_report_path,
        junit_report=junit_report_path,
        collect_only=collect_only,
        failfast=failfast,
        framework=framework,
        settings_module=django_settings,
        extra_args=extra_args,
    )
    
    return result

@app.command("init")
def init(
    directory: Path = typer.Argument(
        ".", help="Project root directory"
    ),
    framework: Optional[str] = typer.Option(
        None, "--framework", "-f", help="Web framework (django, flask, fastapi)"
    ),
    create_examples: bool = typer.Option(
        True, "--examples/--no-examples", help="Create example test files"
    ),
    non_interactive: bool = typer.Option(
        False, "--non-interactive", help="Run in non-interactive mode"
    ),
):
    """Initialize pytest configuration for a project."""
    directory_str = str(directory)
    interactive = not non_interactive
    
    # Get framework if not provided
    if not framework and interactive:
        project_info = detect_project_type(directory_str)
        detected_framework = project_info.get("framework")
        
        frameworks = ["django", "flask", "fastapi", "other", "none"]
        if detected_framework and detected_framework in frameworks:
            default_framework = detected_framework
        else:
            default_framework = "none"
        
        framework = Prompt.ask(
            "Select framework",
            choices=frameworks,
            default=default_framework
        )
        
        if framework == "other":
            framework = None
    
    # Configure pytest
    success = configure_pytest(
        directory=directory_str,
        framework=framework,
        create_example_tests=create_examples,
        interactive=interactive,
    )
    
    if success:
        return 0
    else:
        return 1

@app.command("info")
def info(
    directory: Path = typer.Argument(
        ".", help="Project directory"
    ),
):
    """Show information about the test configuration."""
    directory_str = str(directory)
    project_info = detect_project_type(directory_str)
    
    # Basic testing info
    console.print(Panel.fit("Test Configuration Information", style="bold blue"))
    
    # Framework detection
    framework = project_info.get("framework")
    if framework:
        console.print(f"Detected framework: [bold green]{framework}[/bold green]")
    else:
        console.print("No framework detected")
    
    # Test directory
    test_path = Path(directory_str) / "tests"
    if test_path.exists():
        test_count = len(list(test_path.glob("test_*.py")))
        console.print(f"Test directory: [green]{test_path}[/green]")
        console.print(f"Test files: [green]{test_count}[/green]")
    else:
        console.print("Test directory: [yellow]Not found[/yellow]")
    
    # Configuration files
    config_files = ["pytest.ini", "pyproject.toml", "conftest.py"]
    for config_file in config_files:
        config_path = Path(directory_str) / config_file
        if config_path.exists():
            console.print(f"Configuration: [green]{config_file}[/green]")
    
    # Suggested settings
    if "suggested_settings" in project_info and project_info["suggested_settings"]:
        console.print("\nSuggested settings:")
        for key, value in project_info["suggested_settings"].items():
            if isinstance(value, list):
                console.print(f"  {key}: [green]{', '.join(value)}[/green]")
            else:
                console.print(f"  {key}: [green]{value}[/green]")
    
    return 0

@app.command("tdd")
def tdd(
    test_path: Path = typer.Argument(
        ..., help="Path to test file or directory to watch"
    ),
    command: Optional[str] = typer.Option(
        None, "--command", "-c", 
        help="Command to run when tests pass (e.g., 'pytest {file}')"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Enable verbose output"
    ),
):
    """
    Run tests in TDD (Test-Driven Development) mode with file watching.
    
    This will watch for changes and automatically run tests.
    """
    try:
        import watchdog
    except ImportError:
        console.print("[bold red]watchdog package is required for TDD mode[/bold red]")
        console.print("Install with: [bold]pip install watchdog[/bold]")
        return 1
    
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    import time
    import subprocess
    
    class TestEventHandler(FileSystemEventHandler):
        def __init__(self, test_path, command, verbose):
            self.test_path = str(test_path)
            self.command = command
            self.verbose = verbose
            self.last_run = 0
            
        def on_any_event(self, event):
            # Debounce - prevent multiple runs for the same change
            if time.time() - self.last_run < 1:
                return
                
            # Only react to .py file changes
            if event.is_directory or not event.src_path.endswith(".py"):
                return
                
            # Run tests
            self.last_run = time.time()
            self._run_tests(event.src_path)
                
        def _run_tests(self, changed_file):
            console.print(f"\n[bold blue]File changed: {changed_file}[/bold blue]")
            
            if self.command:
                cmd = self.command.format(file=changed_file)
                console.print(f"Running command: [bold]{cmd}[/bold]")
                subprocess.run(cmd, shell=True)
            else:
                # Default to running pytest on the test path
                console.print(f"Running tests in: [bold]{self.test_path}[/bold]")
                args = [self.test_path]
                if self.verbose:
                    args.append("-v")
                run_tests(test_paths=args)
    
    path = test_path.resolve()
    if not path.exists():
        console.print(f"[bold red]Path does not exist: {path}[/bold red]")
        return 1
    
    watch_dir = path if path.is_dir() else path.parent
    
    console.print(f"[bold green]TDD mode activated[/bold green]")
    console.print(f"Watching: [bold]{watch_dir}[/bold]")
    console.print("Press Ctrl+C to stop")
    
    # Run tests immediately
    handler = TestEventHandler(path, command, verbose)
    handler._run_tests(str(path))
    
    # Set up watchdog
    observer = Observer()
    observer.schedule(handler, str(watch_dir), recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        console.print("[bold]TDD mode stopped[/bold]")
    
    observer.join()
    return 0 