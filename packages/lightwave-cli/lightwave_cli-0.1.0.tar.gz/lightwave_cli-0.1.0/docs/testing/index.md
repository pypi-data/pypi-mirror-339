# Lightwave Testing Tools

The Lightwave Testing Tools provide a comprehensive, centralized command-line interface for managing pytest configurations and running tests across different types of Python projects. These tools integrate the best practices for testing Django, Flask, and FastAPI applications, with support for Test-Driven Development (TDD) and various advanced testing features.

## Repository Information

The testing tools are part of the [lightwave-dev-tools](https://github.com/kiwi-dev-la/lightwave-dev-tools) repository, which provides a collection of development utilities for Lightwave projects.

## Overview

The testing tools are designed to simplify test setup, configuration, and execution with a focus on:

- **Framework-aware testing**: Automatically detects project frameworks and configures testing appropriately
- **Simplified configuration**: Interactive setup for test environments with sensible defaults
- **Centralized command interface**: A single CLI tool for all testing operations
- **Rich reporting**: Multiple report formats and visualization options
- **Development workflow integration**: Support for TDD workflow with file watching

## Installation

The testing tools are included in the Lightwave Dev Tools package:

```bash
# Install with pip
pip install lightwave-dev-tools

# Or update an existing installation
pip install --upgrade lightwave-dev-tools

# Verify installation
lightwave-dev test --help
```

## Quick Start

### Setting Up Testing for a Project

To initialize testing for a new or existing project:

```bash
# Navigate to your project directory
cd your-project

# Initialize testing configuration
lightwave-dev test init
```

This will:
1. Detect your project's framework (Django, Flask, FastAPI, or other)
2. Create a basic test directory structure
3. Set up appropriate pytest configuration
4. Create sample test files for your framework

### Running Tests

Run all tests in your project:

```bash
lightwave-dev test run
```

Run specific test files or directories:

```bash
lightwave-dev test run tests/unit/
lightwave-dev test run tests/integration/test_api.py
```

Filter tests by markers or keywords:

```bash
lightwave-dev test run --marker integration
lightwave-dev test run --keyword "api"
```

## Test Configuration

### Interactive Configuration

The `lightwave-dev test init` command provides an interactive setup experience:

```bash
lightwave-dev test init
```

You'll be prompted to:
1. Confirm the detected framework or select a different one
2. Choose which pytest plugins to include
3. Set up example test files
4. Configure custom test markers

### Non-Interactive Configuration

For CI/CD environments or scripted setups, use non-interactive mode:

```bash
lightwave-dev test init --framework django --non-interactive
```

### Framework-Specific Configuration

Configure testing for specific frameworks:

```bash
# Django testing setup
lightwave-dev test init --framework django

# FastAPI testing setup
lightwave-dev test init --framework fastapi

# Flask testing setup
lightwave-dev test init --framework flask
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
lightwave-dev test run

# Run with verbose output
lightwave-dev test run --verbose
```

### Test Selection

```bash
# Run tests from specific directories or files
lightwave-dev test run tests/unit/ tests/integration/test_auth.py

# Run tests with specific markers
lightwave-dev test run --marker integration
lightwave-dev test run --marker "unit or integration"

# Run tests by keyword
lightwave-dev test run --keyword "auth"

# List tests without running them
lightwave-dev test run --collect-only
```

### Test Parallelization

```bash
# Run tests in parallel
lightwave-dev test run --parallel

# Specify the number of parallel processes
lightwave-dev test run --parallel --processes 4
```

### Code Coverage

```bash
# Run tests with coverage
lightwave-dev test run --coverage

# Generate HTML coverage report
lightwave-dev test run --coverage --cov-report html

# Generate multiple report types
lightwave-dev test run --coverage --cov-report "term,html,xml"
```

### Test Reports

```bash
# Generate HTML report
lightwave-dev test run --html=report.html

# Generate JUnit XML report (for CI integration)
lightwave-dev test run --junit=junit.xml
```

## Test-Driven Development (TDD)

The TDD mode watches for file changes and automatically runs tests:

```bash
# Watch a test file and run it when changes are detected
lightwave-dev test tdd tests/test_feature.py

# Watch with verbose output
lightwave-dev test tdd tests/test_feature.py --verbose

# Watch with a custom command
lightwave-dev test tdd tests/test_feature.py --command "pytest {file} -v"
```

This is particularly useful for maintaining a rapid feedback loop during development.

## Framework-Specific Features

### Django Testing

The Django testing support includes:

- Automatic detection of Django settings module
- Database test configuration
- REST framework client fixtures
- User authentication fixtures

Example with Django-specific options:

```bash
# Run tests with specific Django settings
lightwave-dev test run --ds=myproject.settings.test

# Run only models tests
lightwave-dev test run --marker models
```

### FastAPI Testing

FastAPI testing includes:

- Async test support
- TestClient setup for API testing
- Dependency mocking utilities

Example:

```bash
# Run API tests
lightwave-dev test run --marker api

# Run async tests with specific timeout
lightwave-dev test run --marker async --timeout 10
```

### Flask Testing

Flask testing includes:

- Application factory testing
- Blueprint testing
- Route testing fixtures

Example:

```bash
# Run Flask route tests
lightwave-dev test run --marker routes
```

## Project Analysis

Get information about the test configuration and suggested settings:

```bash
lightwave-dev test info
```

This command analyzes your project and provides information about:

- Detected framework
- Test directory structure
- Existing test files
- Configuration settings
- Recommended plugins and settings

## Command Reference

### `lightwave-dev test init`

Initialize pytest configuration for a project.

Options:
- `--framework, -f`: Web framework (django, flask, fastapi)
- `--examples/--no-examples`: Create example test files
- `--non-interactive`: Run in non-interactive mode

### `lightwave-dev test run`

Run tests with pytest.

Options:
- Test selection:
  - Paths to test files or directories (arguments)
  - `--marker, -m`: Select tests with specific pytest markers
  - `--keyword, -k`: Select tests by keyword expressions
- Output options:
  - `--verbose, -v`: Enable verbose output
  - `--collect-only`: Only collect tests, don't run them
- Coverage options:
  - `--coverage, -c`: Enable code coverage
  - `--cov-report`: Coverage report format (term, html, xml, annotate)
- Performance options:
  - `--parallel, -p`: Run tests in parallel
  - `--processes, -n`: Number of processes for parallel testing
  - `--timeout, -t`: Test timeout in seconds
- Report options:
  - `--html`: Generate HTML report
  - `--junit`: Generate JUnit XML report
- Execution options:
  - `--failfast, -x`: Stop on first failure
  - `--config`: Path to pytest config file
- Framework options:
  - `--framework`: Project framework (django, flask, fastapi)
  - `--ds`: Django settings module
- Additional options:
  - `--extra`: Additional pytest arguments

### `lightwave-dev test tdd`

Run tests in TDD (Test-Driven Development) mode with file watching.

Options:
- Path to test file or directory to watch (argument)
- `--command, -c`: Command to run when tests pass
- `--verbose, -v`: Enable verbose output

### `lightwave-dev test info`

Show information about the test configuration.

Options:
- Path to project directory (argument, defaults to current directory)

## Test Directory Structure

A typical test directory structure created by the initialization tool:

```
tests/
├── conftest.py           # Common test fixtures and configuration
├── unit/                 # Unit tests directory
│   ├── test_models.py    # Model tests
│   └── test_utils.py     # Utility tests
├── integration/          # Integration tests directory
│   ├── test_api.py       # API integration tests
│   └── test_services.py  # Service integration tests
└── e2e/                  # End-to-end tests directory
    └── test_flows.py     # End-to-end workflow tests
```

## Best Practices

### Test Organization

1. **Use markers for categorization**: Markers help organize tests by type, component, or feature
   ```python
   @pytest.mark.unit
   @pytest.mark.models
   def test_model_validation():
       # Test model validation logic
   ```

2. **Leverage fixtures for common setup**: Define reusable fixtures in conftest.py
   ```python
   @pytest.fixture
   def test_user():
       # Create and return a test user
   ```

3. **Group tests by component**: Organize test files by the components they test

### Test-Driven Development

1. Use the TDD mode to automatically run tests on file changes
2. Start with a failing test, then implement the feature
3. Keep the feedback loop tight with fast-running tests

### Continuous Integration

1. Use the non-interactive mode for CI environments
2. Generate JUnit XML reports for CI integration
3. Use coverage reports to maintain quality standards

## Examples

### Basic Unit Test

```python
import pytest

@pytest.mark.unit
def test_add_function():
    from myapp.utils import add
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
```

### Django Model Test

```python
import pytest

@pytest.mark.django_db
@pytest.mark.models
def test_user_creation(django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpassword"
    )
    assert user.username == "testuser"
    assert user.email == "test@example.com"
```

### FastAPI Endpoint Test

```python
import pytest
from fastapi.testclient import TestClient

@pytest.mark.api
def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

### Flask Route Test

```python
import pytest

@pytest.mark.routes
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to Flask" in response.data
```

## Troubleshooting

### Common Issues

1. **Fixture not found errors**:
   - Check if the fixture is defined in your conftest.py
   - Make sure you've initialized testing for your framework

2. **Import errors in tests**:
   - Make sure the Python path is correctly set
   - Use `base_dir` fixture to resolve paths

3. **Database errors in Django tests**:
   - Ensure the `@pytest.mark.django_db` marker is used
   - Check Django settings (use `--ds` option)

### Getting Help

If you encounter issues with the testing tools:

1. Check the detailed help for the specific command:
   ```bash
   lightwave-dev test run --help
   ```

2. View the project configuration information:
   ```bash
   lightwave-dev test info
   ```

3. Refer to the [pytest documentation](https://docs.pytest.org/) for underlying pytest functionality
4. Visit the [Lightwave Dev Tools repository](https://github.com/kiwi-dev-la/lightwave-dev-tools) for source code and issues

## Conclusion

The Lightwave Testing Tools provide a powerful, unified interface for managing tests across different Python frameworks. By combining the flexibility of pytest with framework-specific enhancements and a streamlined CLI, these tools help developers maintain high-quality code with efficient testing workflows. 