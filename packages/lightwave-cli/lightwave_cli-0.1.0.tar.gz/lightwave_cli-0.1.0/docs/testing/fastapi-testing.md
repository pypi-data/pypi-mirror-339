# Testing FastAPI Applications with Lightwave Testing Tools

This guide shows how to effectively test FastAPI applications using the Lightwave Testing Tools. FastAPI is a modern, fast web framework for building APIs with Python, and our testing tools provide specialized support for its unique features.

## Repository Information

The testing tools are part of the [lightwave-dev-tools](https://github.com/kiwi-dev-la/lightwave-dev-tools) repository, which provides a collection of development utilities for Lightwave projects.

## Getting Started

### Installation

First, ensure you have the Lightwave Dev Tools installed:

```bash
pip install lightwave-dev-tools
```

### Initialize Testing for FastAPI

In your FastAPI project directory, initialize testing with FastAPI-specific configuration:

```bash
cd your-fastapi-project
lightwave-dev test init --framework fastapi
```

This will:
1. Create a test directory structure
2. Set up a conftest.py with FastAPI-specific fixtures
3. Configure pytest to support asynchronous testing
4. Create example FastAPI test files

## FastAPI-Specific Testing Features

The Lightwave Testing Tools include several features designed specifically for FastAPI:

### Automatic App and Client Fixtures

The initialization creates useful fixtures in conftest.py:

```python
@pytest.fixture
def app():
    """Create a FastAPI test application."""
    from fastapi import FastAPI
    
    # Create a test app or import your actual app
    # from app.main import app
    app = FastAPI()
    
    @app.get("/test")
    def read_test():
        return {"message": "Test endpoint"}
    
    return app

@pytest.fixture
def client(app):
    """Return a FastAPI test client."""
    from fastapi.testclient import TestClient
    return TestClient(app)
```

These fixtures allow you to easily test FastAPI endpoints without duplicating setup code.

### Async Testing Support

FastAPI relies heavily on async functions, and the Lightwave Testing Tools configures pytest-asyncio for you:

```python
@pytest.mark.async
async def test_async_endpoint(app):
    """Test an async endpoint."""
    @app.get("/async-test")
    async def read_async_test():
        return {"message": "Async test endpoint"}
    
    # Test with sync TestClient
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/async-test")
    assert response.status_code == 200
    assert response.json() == {"message": "Async test endpoint"}
```

### API-Specific Test Markers

The testing tools define FastAPI-specific markers:

- `@pytest.mark.api`: For API endpoint tests
- `@pytest.mark.routes`: For route configuration tests
- `@pytest.mark.async`: For asynchronous function tests

## Writing FastAPI Tests

### Basic Endpoint Test

Test a simple GET endpoint:

```python
import pytest
from fastapi.testclient import TestClient

@pytest.mark.api
def test_read_main(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

### Testing POST Endpoints

Test a POST endpoint with JSON body:

```python
@pytest.mark.api
def test_create_item(client):
    """Test creating an item via POST."""
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 10.5}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 10.5
    assert "id" in data
```

### Testing Path Parameters

Test endpoints with path parameters:

```python
@pytest.mark.api
def test_get_item(client):
    """Test getting an item by ID."""
    # First create an item
    create_response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 10.5}
    )
    item_id = create_response.json()["id"]
    
    # Then get it by ID
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 10.5
    assert data["id"] == item_id
```

### Testing Query Parameters

Test endpoints with query parameters:

```python
@pytest.mark.api
def test_list_items_with_skip_limit(client):
    """Test listing items with skip and limit parameters."""
    # Create multiple items
    for i in range(5):
        client.post(
            "/items/",
            json={"name": f"Item {i}", "price": 10.0 + i}
        )
    
    # Test with query parameters
    response = client.get("/items/?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Should get 2 items
    assert data[0]["name"] == "Item 1"
    assert data[1]["name"] == "Item 2"
```

### Testing Authentication

Test authenticated endpoints:

```python
@pytest.fixture
def auth_client(client):
    """Return a pre-authenticated client."""
    # Perform login
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = response.json()["access_token"]
    
    # Update headers with token
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

@pytest.mark.api
def test_protected_endpoint(auth_client):
    """Test an endpoint that requires authentication."""
    response = auth_client.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
```

## Testing FastAPI Dependencies

### Mocking Dependencies

FastAPI uses dependency injection extensively. Here's how to test with mocked dependencies:

```python
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

# Define a dependency
async def get_db():
    # Real implementation would return a database session
    raise NotImplementedError("Not implemented for production")

app = FastAPI()

@app.get("/items/")
async def read_items(db=Depends(get_db)):
    return {"db": "connected"}

# In your test file
@pytest.fixture
def override_get_db():
    """Override the get_db dependency."""
    return lambda: "test_db"

@pytest.fixture
def test_app(override_get_db):
    """Create a test app with overridden dependencies."""
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/items/")
    async def read_items(db=Depends(override_get_db)):
        return {"db": db}
    
    return app

@pytest.fixture
def test_client(test_app):
    """Return a client for the test app."""
    return TestClient(test_app)

@pytest.mark.api
def test_dependency_override(test_client):
    """Test that the dependency was overridden."""
    response = test_client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {"db": "test_db"}
```

### Using FastAPI's TestClient Dependency Overrides

FastAPI provides a built-in way to override dependencies:

```python
@pytest.mark.api
def test_dependency_override_builtin(client, app):
    """Test using FastAPI's built-in dependency override."""
    # Define a test dependency
    async def override_get_db():
        return "test_db"
    
    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Test with the overridden dependency
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {"db": "test_db"}
    
    # Clean up after test
    app.dependency_overrides = {}
```

## Testing Asynchronous Code

FastAPI's main feature is its support for asynchronous Python. Here's how to test async code:

### Testing Async Endpoints

```python
@pytest.mark.async
async def test_async_endpoint_directly(app):
    """Test an async endpoint directly."""
    @app.get("/async-test")
    async def read_async_test():
        return {"message": "Async test endpoint"}
    
    # Create a client that doesn't run in a separate thread
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    response = client.get("/async-test")
    assert response.status_code == 200
    assert response.json() == {"message": "Async test endpoint"}
```

### Testing Async Dependencies

```python
@pytest.mark.async
async def test_async_dependency(app):
    """Test an endpoint with an async dependency."""
    # Define an async dependency
    async def get_async_data():
        return {"data": "async data"}
    
    @app.get("/async-data")
    async def read_async_data(data=Depends(get_async_data)):
        return data
    
    # Test the endpoint
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    response = client.get("/async-data")
    assert response.status_code == 200
    assert response.json() == {"data": "async data"}
```

## Running FastAPI Tests

Using the Lightwave Testing Tools, you can run FastAPI tests in various ways:

### Basic Test Running

```bash
# Run all FastAPI tests
lightwave-dev test run

# Run API-specific tests
lightwave-dev test run --marker api

# Run async tests
lightwave-dev test run --marker async

# Run specific test file
lightwave-dev test run tests/test_api.py
```

### Using TDD Mode for FastAPI

```bash
# TDD mode for a specific test file
lightwave-dev test tdd tests/test_api.py

# TDD mode for async tests
lightwave-dev test tdd tests/ --command "pytest {file} -m async -v"
```

### Test Coverage

```bash
# Run with coverage
lightwave-dev test run --coverage

# Generate HTML coverage report
lightwave-dev test run --coverage --cov-report html
```

## Integration with Database Testing

For FastAPI applications that use databases, you can set up integrated database testing:

### SQLAlchemy Integration

```python
@pytest.fixture
def db_session():
    """Create a test database session."""
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    
    # Use an in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:")
    
    from app.models import Base
    Base.metadata.create_all(engine)
    
    TestSessionLocal = sessionmaker(bind=engine)
    session = TestSessionLocal()
    
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def override_get_db(db_session):
    """Override the get_db dependency to use the test session."""
    def _get_db():
        try:
            yield db_session
        finally:
            pass
    return _get_db

@pytest.fixture
def test_client(app, override_get_db):
    """Return a client with DB dependency overridden."""
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides = {}
```

### Testing Database Operations

```python
@pytest.mark.api
def test_create_and_read_item(test_client, db_session):
    """Test creating and reading an item with the database."""
    # Create an item
    create_response = test_client.post(
        "/items/",
        json={"name": "DB Test Item", "price": 15.5}
    )
    assert create_response.status_code == 200
    item_id = create_response.json()["id"]
    
    # Verify it was created in the database
    from app.models import Item
    db_item = db_session.query(Item).filter(Item.id == item_id).first()
    assert db_item is not None
    assert db_item.name == "DB Test Item"
    assert db_item.price == 15.5
    
    # Get the item via API
    get_response = test_client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    assert get_response.json() == {
        "id": item_id,
        "name": "DB Test Item",
        "price": 15.5
    }
```

## Best Practices for FastAPI Testing

1. **Use appropriate markers**: Categorize your tests using the built-in markers

2. **Test status codes**: Always verify the HTTP status code in your responses

3. **Test response bodies**: Validate the structure and content of response JSON

4. **Override dependencies**: Use dependency overrides for clean, isolated tests

5. **Use in-memory databases**: For fast tests that don't require external services

6. **Test validation**: FastAPI uses Pydantic for validation, so test with both valid and invalid input

7. **Test error handling**: Verify that errors return appropriate status codes and responses

8. **Separate unit and integration tests**: Use markers to distinguish between test types

## Conclusion

Testing FastAPI applications with Lightwave Testing Tools provides a streamlined workflow for ensuring your API behaves as expected. By leveraging the specialized fixtures, markers, and utilities provided by the Lightwave tools, you can build robust test suites that validate your FastAPI application's behavior thoroughly.

Remember to use the asynchronous testing capabilities when testing async code, override dependencies to isolate your tests, and make use of the various test selection and reporting options to make your testing process efficient and effective. 