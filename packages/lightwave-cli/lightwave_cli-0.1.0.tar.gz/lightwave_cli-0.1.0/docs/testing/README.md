# Lightwave Testing Documentation

Welcome to the Lightwave Testing documentation. This section provides comprehensive guides for using the Lightwave Testing Tools to test Python applications of various types.

## Repository Information

The Lightwave Testing Tools are part of the [lightwave-dev-tools](https://github.com/kiwi-dev-la/lightwave-dev-tools) repository, which provides a collection of development utilities for Lightwave projects.

## Core Documentation

- [**Testing Tools Overview**](./index.md) - Main documentation for the Lightwave Testing Tools
- [**Test-Driven Development Guide**](./tdd-guide.md) - How to implement TDD with Lightwave tools

## Framework-Specific Testing Guides

- [**Django Testing Guide**](./django-testing.md) - Testing Django web applications
- [**FastAPI Testing Guide**](./fastapi-testing.md) - Testing FastAPI applications and APIs

## Getting Started

The Lightwave Testing Tools provide a centralized CLI for pytest configuration and execution. Get started with:

```bash
# Install the Lightwave dev tools
pip install lightwave-dev-tools

# Initialize testing for a project
lightwave-dev test init

# Run tests
lightwave-dev test run
```

## Key Features

- Framework detection and specialized testing support
- Interactive test configuration
- TDD workflow with file watching
- Test running with parallel execution and coverage reports
- Customized fixtures for Django, FastAPI, and more

## Command Reference

| Command | Description |
|---------|-------------|
| `lightwave-dev test init` | Initialize testing for a project |
| `lightwave-dev test run` | Run tests with various options |
| `lightwave-dev test tdd` | Run tests in Test-Driven Development mode |
| `lightwave-dev test info` | Display information about the test configuration |

## More Resources

- [pytest documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://pytest-with-eric.com/)
- [Lightwave Dev Tools Repository](https://github.com/kiwi-dev-la/lightwave-dev-tools) 