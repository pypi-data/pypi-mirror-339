# Test-Driven Development with Lightwave Testing Tools

This guide explains how to use the Lightwave Testing Tools to implement Test-Driven Development (TDD) in your projects. TDD is a software development approach where tests are written before the code they're testing, leading to more robust and maintainable software.

## Repository Information

The testing tools are part of the [lightwave-dev-tools](https://github.com/kiwi-dev-la/lightwave-dev-tools) repository, which provides a collection of development utilities for Lightwave projects.

## Understanding TDD

The TDD workflow follows a simple cycle:

1. **Red**: Write a failing test that defines a function or improvement
2. **Green**: Write the minimal code needed to make the test pass
3. **Refactor**: Clean up the code while keeping tests passing

This cycle is typically repeated many times during development, with each iteration adding a small piece of functionality.

## Setting Up TDD with Lightwave Tools

### Installation

First, ensure you have the Lightwave Dev Tools installed:

```bash
pip install lightwave-dev-tools
```

### Project Setup

Initialize your project for testing:

```bash
# Navigate to your project directory
cd your-project

# Initialize testing
lightwave-dev test init

# If you know your framework
lightwave-dev test init --framework fastapi
```

## Using TDD Mode

The Lightwave Testing Tools include a dedicated TDD mode that automatically watches for file changes and runs relevant tests:

```bash
# Basic TDD mode
lightwave-dev test tdd tests/test_feature.py

# TDD with verbose output
lightwave-dev test tdd tests/test_feature.py --verbose
```

### Customizing the TDD Commands

You can customize how tests are run when files change:

```bash
# Custom test command with more control
lightwave-dev test tdd tests/ --command "pytest {file} -v"
```

The `{file}` placeholder will be replaced with the path of the changed file.

## TDD Workflow Example

Let's walk through a complete TDD cycle using the Lightwave Testing Tools.

### 1. Create a Test File

First, create a test file for the feature you want to implement:

```python
# tests/unit/test_calculator.py
import pytest

@pytest.mark.unit
def test_add():
    """Test the add function of our calculator."""
    from myapp.calculator import add
    
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

### 2. Start TDD Mode

Start the TDD mode to watch for changes:

```bash
lightwave-dev test tdd tests/unit/test_calculator.py
```

At this point, the test will fail because we haven't implemented the `add` function yet.

### 3. Implement the Function

Now, create the implementation file:

```python
# myapp/calculator.py
def add(a, b):
    """Add two numbers and return the result."""
    return a + b
```

As soon as you save this file, the TDD mode will detect the change and run the test again. The test should now pass.

### 4. Extend with a New Test

Add a new test for another calculator function:

```python
# tests/unit/test_calculator.py
# ... existing code ...

@pytest.mark.unit
def test_multiply():
    """Test the multiply function of our calculator."""
    from myapp.calculator import multiply
    
    assert multiply(2, 3) == 6
    assert multiply(-1, 4) == -4
    assert multiply(0, 5) == 0
```

Save the file. The TDD mode will detect the change and run the tests. The new test will fail because we haven't implemented the `multiply` function yet.

### 5. Implement the New Function

Update the implementation file:

```python
# myapp/calculator.py
def add(a, b):
    """Add two numbers and return the result."""
    return a + b

def multiply(a, b):
    """Multiply two numbers and return the result."""
    return a * b
```

Save the file. The TDD mode will detect the change and run the tests again. Both tests should now pass.

## TDD Tips for Different Frameworks

### Django TDD

When doing TDD with Django, use the following approach:

```bash
# Initialize testing for Django
lightwave-dev test init --framework django

# Start TDD mode for model tests
lightwave-dev test tdd tests/test_models.py

# Use custom command for view tests
lightwave-dev test tdd tests/test_views.py --command "pytest {file} --ds=myproject.settings.test"
```

Django-specific tips:
- Use the `@pytest.mark.django_db` decorator for tests that need database access
- Leverage Django's `TestCase` through pytest-django
- Mock external services and APIs to isolate tests

### FastAPI TDD

For FastAPI applications:

```bash
# Initialize testing for FastAPI
lightwave-dev test init --framework fastapi

# Start TDD mode for API tests
lightwave-dev test tdd tests/test_api.py
```

FastAPI-specific tips:
- Use the `client` fixture to test endpoints
- Test with different inputs to verify validation
- Use async tests for async endpoints

### Flask TDD

For Flask applications:

```bash
# Initialize testing for Flask
lightwave-dev test init --framework flask

# Start TDD mode for route tests
lightwave-dev test tdd tests/test_routes.py
```

Flask-specific tips:
- Use the `client` fixture to make requests
- Test response codes and content
- Check for correct template rendering

## Advanced TDD Techniques

### Parameterized Tests

Use pytest's parameterization to test multiple inputs:

```python
@pytest.mark.parametrize("input_a,input_b,expected", [
    (1, 2, 3),
    (-1, 1, 0),
    (0, 0, 0),
    (100, -100, 0),
])
def test_add_parameterized(input_a, input_b, expected):
    from myapp.calculator import add
    assert add(input_a, input_b) == expected
```

### Test Fixtures

Create fixtures for common test setups:

```python
@pytest.fixture
def calculator():
    """Return a calculator instance."""
    from myapp.calculator import Calculator
    return Calculator()

def test_calculator_methods(calculator):
    assert calculator.add(1, 2) == 3
    assert calculator.multiply(2, 3) == 6
```

### Mocking External Services

Use pytest-mock to replace external dependencies:

```python
def test_api_client(mocker):
    # Mock the external API
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"data": "mocked data"}
    
    # Replace requests.get with our mock
    mocker.patch("requests.get", return_value=mock_response)
    
    # Now test our code that uses requests.get
    from myapp.client import get_data
    result = get_data()
    assert result == {"data": "mocked data"}
```

## TDD Best Practices

1. **Keep tests focused**: Each test should verify a single aspect of behavior

2. **Use descriptive test names**: The test name should explain what's being tested

3. **Maintain test independence**: Tests shouldn't depend on each other

4. **Balance coverage and practicality**: Aim for good coverage, but focus on critical paths

5. **Refactor regularly**: Clean up both test and production code as you go

6. **Commit after each passing test**: This creates a history of working states

7. **Keep the feedback loop fast**: Tests should run quickly to maintain flow

## TDD in CI/CD Pipelines

Integrate your TDD-developed tests into CI/CD:

```bash
# Run all tests in CI
lightwave-dev test run --coverage --junit=junit.xml

# Run with specific markers
lightwave-dev test run --marker "unit or integration" --coverage
```

Set up your CI pipeline to:
1. Run tests on every push
2. Generate coverage reports
3. Fail the build if tests fail
4. Track test metrics over time

## Conclusion

Test-Driven Development with the Lightwave Testing Tools provides a structured, efficient approach to software development. By writing tests first and leveraging the automated testing capabilities of the Lightwave Dev Tools, you can build more reliable software while maintaining rapid development cycles.

Remember the TDD cycle: Red, Green, Refactor. Write a failing test, make it pass with the simplest code possible, then clean up your code while keeping the tests passing. Repeat this process for every feature or change, and you'll build a comprehensive test suite alongside your application.

Happy testing! 