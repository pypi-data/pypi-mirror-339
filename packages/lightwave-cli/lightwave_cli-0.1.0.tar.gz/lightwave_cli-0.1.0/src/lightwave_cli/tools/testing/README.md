# LightWave Testing Tools

A comprehensive testing toolkit for various types of Python projects, including Django, Flask, and FastAPI applications. The testing module provides a centralized CLI for managing pytest configurations and running tests with sensible defaults.

## Features

- **Framework Detection**: Automatically detects project frameworks and suggests appropriate configurations
- **Test Configuration**: Interactive setup of pytest configurations for different project types
- **Test Runner**: Run tests with customizable options for coverage, reporting, and parallelization
- **TDD Mode**: Watch for file changes and automatically run tests for Test-Driven Development
- **Multi-Framework Support**: Specialized testing features for Django, Flask, and FastAPI projects

## Installation

The testing tools are included in the LightWave CLI. Make sure you have the CLI installed and updated.

```bash
# Install with pip
pip install lightwave-cli

# Or update an existing installation
pip install --upgrade lightwave-cli
```

## Usage

### Running Tests

```bash
# Run all tests in the tests directory
lightwave test run

# Run specific test files or directories
lightwave test run tests/test_api.py

# Run tests with specific markers
lightwave test run --marker integration

# Run tests with coverage
lightwave test run --coverage --cov-report html

# Run tests in parallel
lightwave test run --parallel
```

### Setting Up Testing

```bash
# Initialize testing for a project
lightwave test init

# Configure for a specific framework
lightwave test init --framework django

# Non-interactive configuration
lightwave test init --framework fastapi --non-interactive
```

### Test-Driven Development (TDD)

```bash
# Watch a test file and run tests when changes are detected
lightwave test tdd tests/test_feature.py

# Watch with custom command
lightwave test tdd tests/test_feature.py --command "pytest {file} -v"
```

### Get Test Info

```bash
# Show information about the current test configuration
lightwave test info
```

## Framework-Specific Features

### Django

- Automatic detection of Django settings
- Creation of appropriate test fixtures (db, client, etc.)
- Support for Django REST framework testing

### FastAPI

- Async test support
- API endpoint testing fixtures
- Test client setup

### Flask

- Flask app test fixtures
- Blueprint testing support
- Route testing utilities

## Example: Setting Up a New Project for Testing

1. Initialize testing configuration:
   ```bash
   lightwave test init
   ```

2. Follow the interactive prompts to select your framework and plugins

3. Run the tests:
   ```bash
   lightwave test run
   ```

4. Generate a coverage report:
   ```bash
   lightwave test run --coverage --cov-report html
   ```

## Full Command Reference

See the CLI help for complete documentation:

```bash
lightwave test --help
lightwave test run --help
lightwave test init --help
lightwave test tdd --help
lightwave test info --help
``` 