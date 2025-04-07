"""
Integration tests demonstrating fixture usage.
"""

import pytest
import os

@pytest.mark.integration
def test_base_dir_structure(base_dir):
    """Test that the base directory has the expected structure."""
    assert base_dir.exists()
    assert (base_dir / "src").exists()
    assert (base_dir / "tests").exists()

@pytest.mark.integration
def test_sample_data_structure(sample_data):
    """Test the structure of the sample data fixture."""
    assert "name" in sample_data
    assert "version" in sample_data
    assert "commands" in sample_data
    assert "test" in sample_data["commands"]

@pytest.mark.integration
def test_temp_file_fixture(temp_file):
    """Test the temp_file fixture."""
    assert temp_file.exists()
    with open(temp_file, "r") as f:
        content = f.read()
    assert content == "Test content"
    
    # Modify the file and verify changes
    with open(temp_file, "a") as f:
        f.write("\nAdditional content")
    
    with open(temp_file, "r") as f:
        updated_content = f.read()
    
    assert "Additional content" in updated_content 