"""
UV Integration

Functions for integrating with the UV package manager.
"""
import os
import subprocess
from pathlib import Path
from typing import List, Optional, Union

def run_uv_command(
    args: List[str], 
    cwd: Optional[Union[str, Path]] = None, 
    capture_output: bool = False
) -> subprocess.CompletedProcess:
    """
    Run a UV command with the given arguments.
    
    Args:
        args: List of arguments to pass to UV
        cwd: Working directory to run the command in
        capture_output: Whether to capture the command output
    
    Returns:
        CompletedProcess instance with command result
    """
    command = ["uv"] + args
    
    return subprocess.run(
        command,
        cwd=cwd,
        capture_output=capture_output,
        text=True,
        check=False  # Don't raise an exception on non-zero exit
    )

def ensure_uv_installed() -> bool:
    """
    Check if UV is installed and available.
    
    Returns:
        True if UV is installed, False otherwise
    """
    try:
        result = subprocess.run(
            ["uv", "--version"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

def create_virtual_env(
    path: Optional[Union[str, Path]] = None,
    python: Optional[str] = None
) -> bool:
    """
    Create a virtual environment using UV.
    
    Args:
        path: Path where to create the virtual environment
        python: Python version to use
    
    Returns:
        True if successful, False otherwise
    """
    args = ["venv"]
    
    if path:
        args.append(str(path))
    
    if python:
        args.extend(["--python", python])
    
    result = run_uv_command(args)
    return result.returncode == 0

def install_package(
    package_spec: str,
    editable: bool = False,
    dev: bool = False,
    cwd: Optional[Union[str, Path]] = None
) -> bool:
    """
    Install a package using UV.
    
    Args:
        package_spec: Package specification (name, path, or URL)
        editable: Whether to install in editable mode
        dev: Whether to install as a development dependency
        cwd: Working directory
    
    Returns:
        True if successful, False otherwise
    """
    args = ["pip", "install"]
    
    if editable:
        args.append("-e")
    
    if dev:
        args.append("--dev")
    
    args.append(package_spec)
    
    result = run_uv_command(args, cwd=cwd)
    return result.returncode == 0 