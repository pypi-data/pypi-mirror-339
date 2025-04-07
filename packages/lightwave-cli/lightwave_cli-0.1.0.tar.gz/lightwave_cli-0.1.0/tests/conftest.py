"""
Pytest configuration and fixtures.
"""

import pytest
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).parent.parent

@pytest.fixture
def base_dir():
    """Return the base directory of the project."""
    return BASE_DIR

@pytest.fixture
def sample_data():
    """Return sample data for tests."""
    return {
        "name": "LightWave CLI",
        "version": "0.1.0",
        "commands": ["docs", "agent", "uv", "test"],
    }

@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file for testing."""
    file_path = tmp_path / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("Test content")
    return file_path 