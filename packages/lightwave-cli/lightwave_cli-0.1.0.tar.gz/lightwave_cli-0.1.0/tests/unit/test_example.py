"""
Example unit tests for the testing module.
"""

import pytest

@pytest.mark.unit
def test_basic_assertion():
    """Test a basic assertion."""
    assert True

@pytest.mark.unit
def test_string_methods():
    """Test basic string methods."""
    value = "hello world"
    assert value.startswith("hello")
    assert value.endswith("world")
    assert "hello" in value
    assert len(value) == 11

@pytest.mark.parametrize("input_value,expected", [
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input_value, expected):
    """Test squaring values with parametrize."""
    assert input_value ** 2 == expected 