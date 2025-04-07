"""
Testing utilities for LightWave projects.

This module provides centralized pytest testing utilities for different types of projects.
"""

from .runner import run_tests
from .configurator import configure_pytest

__all__ = ["run_tests", "configure_pytest"] 