#!/usr/bin/env python3
"""
LightWave CLI

Main entry point for the LightWave command-line interface.
"""

import sys
import typer
import os
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = typer.Typer(help="LightWave ecosystem CLI tools")
console = Console()

# Create subcommands
docs_app = typer.Typer(help="Documentation management commands")
agent_app = typer.Typer(help="AI agent commands")
uv_app = typer.Typer(help="UV package manager commands")
test_app = typer.Typer(help="Testing and quality tools")

# Register subcommands
app.add_typer(docs_app, name="docs")
app.add_typer(agent_app, name="agent")
app.add_typer(uv_app, name="uv")
app.add_typer(test_app, name="test")

# Documentation commands
@docs_app.command("sync")
def sync_docs(
    base_dir: str = typer.Option(".", help="Base directory containing docs to update"),
    repo_url: str = typer.Option(
        os.environ.get("DOCS_REPO_URL", "https://github.com/joelschaeffer/lightwave-eco-system-docs.git"), 
        help="GitHub repository URL"
    ),
    branch: str = typer.Option(
        os.environ.get("DOCS_BRANCH", "main"), 
        help="Branch or commit hash to use"
    ),
    docs_subdir: str = typer.Option("docs", help="Subdirectory in repo containing docs"),
    local_repo: Optional[str] = typer.Option(
        None, help="Path to local repository (if already cloned)"
    )
):
    """Synchronize documentation from a GitHub repository to the local project."""
    from lightwave_cli.tools.docs_sync import sync_docs as run_sync_docs
    
    if local_repo:
        repo_url = local_repo
        console.print(f"[bold blue]Using local repository at {local_repo}[/bold blue]")
    
    try:
        update_count = run_sync_docs(base_dir, repo_url, branch, docs_subdir)
        console.print(f"[bold green]Documentation sync complete! Updated {update_count} files.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        return 1
    
    return 0

# Agent commands
@agent_app.command("run")
def run_agent(
    agent: str = typer.Argument(..., help="Name of the agent to run"),
    prompt: str = typer.Argument(..., help="Prompt to send to the agent"),
    model: str = typer.Option(None, help="Override the default model"),
    temperature: float = typer.Option(None, help="Override the default temperature"),
    max_tokens: int = typer.Option(None, help="Override the default max tokens"),
    env_file: Optional[Path] = typer.Option(
        None, help="Path to .env file with API keys"
    ),
    options: Optional[List[str]] = typer.Option(
        None, help="Additional options in key=value format"
    )
):
    """Run an AI agent with the specified prompt."""
    import os
    from dotenv import load_dotenv
    
    # Load environment variables if env_file is provided
    if env_file and env_file.exists():
        load_dotenv(env_file)
        console.print(f"[bold blue]Loaded environment from {env_file}[/bold blue]")
    
    # Parse additional options
    opts = {}
    if options:
        for opt in options:
            if "=" in opt:
                key, value = opt.split("=", 1)
                opts[key.strip()] = value.strip()
    
    try:
        # Import the appropriate agent dynamically
        try:
            module = __import__(f"lightwave_cli.agents.{agent}", fromlist=["agent"])
            agent_instance = module.agent
        except ImportError:
            console.print(f"[bold red]Agent '{agent}' not found[/bold red]")
            return 1
        
        # Set overrides
        overrides = {}
        if model:
            overrides["model_name"] = model
        if temperature is not None:
            overrides["temperature"] = temperature
        if max_tokens is not None:
            overrides["max_tokens"] = max_tokens
        
        # Run the agent
        response = agent_instance.run(prompt=prompt, **overrides, **opts)
        
        if response.success:
            console.print(f"[bold green]{response.message}[/bold green]")
            if response.data:
                import json
                console.print(json.dumps(response.data, indent=2))
        else:
            console.print(f"[bold red]{response.message}[/bold red]")
            if response.errors:
                for error in response.errors:
                    console.print(f"[red]- {error}[/red]")
            return 1
        
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        return 1
    
    return 0

# Testing commands
# Include testing commands from tools/testing/cli.py
from lightwave_cli.tools.testing.cli import app as testing_cli
test_app.add_typer(testing_cli)

# UV package manager commands
@uv_app.command("install")
def uv_install(
    package: str = typer.Argument(..., help="Package specification to install"),
    editable: bool = typer.Option(False, "--editable", "-e", help="Install in editable mode"),
    dev: bool = typer.Option(False, "--dev", "-d", help="Install as dev dependency"),
    path: Optional[Path] = typer.Option(None, "--path", "-p", help="Path to run the command in")
):
    """Install a package using UV."""
    from lightwave_cli.tools.uv_integration import ensure_uv_installed, install_package
    
    if not ensure_uv_installed():
        console.print("[bold red]Error: UV is not installed or not in PATH[/bold red]")
        console.print("Install UV with: curl -sSf https://astral.sh/uv/install.sh | sh")
        return 1
    
    try:
        console.print(f"Installing {package}...")
        success = install_package(package, editable=editable, dev=dev, cwd=path)
        
        if success:
            console.print(f"[bold green]Successfully installed {package}[/bold green]")
        else:
            console.print(f"[bold red]Failed to install {package}[/bold red]")
            return 1
            
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        return 1
    
    return 0

@uv_app.command("venv")
def uv_venv(
    path: Optional[Path] = typer.Argument(None, help="Path where to create the virtual environment"),
    python: Optional[str] = typer.Option(None, "--python", "-p", help="Python version to use")
):
    """Create a virtual environment using UV."""
    from lightwave_cli.tools.uv_integration import ensure_uv_installed, create_virtual_env
    
    if not ensure_uv_installed():
        console.print("[bold red]Error: UV is not installed or not in PATH[/bold red]")
        console.print("Install UV with: curl -sSf https://astral.sh/uv/install.sh | sh")
        return 1
    
    try:
        path_str = str(path) if path else ".venv"
        console.print(f"Creating virtual environment at {path_str}...")
        success = create_virtual_env(path=path, python=python)
        
        if success:
            console.print(f"[bold green]Virtual environment created at {path_str}[/bold green]")
            console.print("Activate with:")
            if sys.platform == "win32":
                console.print(f"    {path_str}\\Scripts\\activate")
            else:
                console.print(f"    source {path_str}/bin/activate")
        else:
            console.print(f"[bold red]Failed to create virtual environment[/bold red]")
            return 1
            
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        return 1
    
    return 0

@uv_app.command("run")
def uv_run(
    command: List[str] = typer.Argument(..., help="Command to run with UV")
):
    """Run a command using UV."""
    from lightwave_cli.tools.uv_integration import ensure_uv_installed, run_uv_command
    
    if not ensure_uv_installed():
        console.print("[bold red]Error: UV is not installed or not in PATH[/bold red]")
        console.print("Install UV with: curl -sSf https://astral.sh/uv/install.sh | sh")
        return 1
    
    try:
        result = run_uv_command(command)
        return result.returncode
            
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")
        return 1

def main():
    """Run the CLI application."""
    app()

if __name__ == "__main__":
    sys.exit(main()) 