# Testing Django Applications with Lightwave Testing Tools

This guide provides a comprehensive approach to testing Django applications using the Lightwave Testing Tools. Django is a powerful web framework for Python, and our testing tools offer specialized features to make testing Django projects simpler and more effective.

## Repository Information

The testing tools are part of the [lightwave-dev-tools](https://github.com/kiwi-dev-la/lightwave-dev-tools) repository, which provides a collection of development utilities for Lightwave projects.

## Getting Started

### Installation

First, ensure you have the Lightwave Dev Tools installed:

```bash
pip install lightwave-dev-tools
```

### Initialize Testing for Django

In your Django project directory, set up testing with Django-specific configuration:

```bash
cd your-django-project
lightwave-dev test init --framework django
```

This will:
1. Create a test directory structure
2. Set up a conftest.py with Django-specific fixtures
3. Configure pytest to work with Django's test system
4. Create example Django test files

## Django-Specific Testing Features

The Lightwave Testing Tools include several features designed specifically for Django:

### Automatic Settings Detection

The tools automatically detect your Django settings module and configure pytest to use it:

```bash
# Run tests with detected settings
lightwave-dev test run

# Specify a different settings module
lightwave-dev test run --ds=myproject.settings.test
```

### Database Access Fixtures

The initialization creates useful fixtures in conftest.py:

```python
# Standard Django database fixture
# The 'db' fixture is provided by pytest-django

@pytest.fixture
def api_client():
    """Return a Django REST framework API client."""
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def authenticated_client(db, django_user_model):
    """Return an authenticated client."""
    from django.test import Client
    
    username = "testuser"
    password = "testpassword"
    
    django_user_model.objects.create_user(username=username, password=password)
    client = Client()
    client.login(username=username, password=password)
    
    return client
```

### Django-Specific Test Markers

The tools define Django-specific markers:

- `@pytest.mark.django_db`: Marks tests that need database access
- `@pytest.mark.models`: For model-related tests
- `@pytest.mark.views`: For view tests
- `@pytest.mark.forms`: For form tests
- `@pytest.mark.urls`: For URL configuration tests

## Writing Django Tests

### Model Tests

Test Django models:

```python
import pytest

@pytest.mark.django_db
@pytest.mark.models
def test_user_creation(django_user_model):
    """Test creating a user."""
    user = django_user_model.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="password123"
    )
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.check_password("password123")

@pytest.mark.django_db
@pytest.mark.models
def test_custom_model():
    """Test a custom model."""
    from myapp.models import Product
    
    product = Product.objects.create(
        name="Test Product",
        price=10.99,
        description="A test product"
    )
    
    assert product.name == "Test Product"
    assert product.price == 10.99
    assert product.description == "A test product"
    assert str(product) == "Test Product"  # Test __str__ method
```

### View Tests

Test Django views:

```python
@pytest.mark.django_db
@pytest.mark.views
def test_home_view(client):
    """Test the home view."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in str(response.content)

@pytest.mark.django_db
@pytest.mark.views
def test_protected_view(authenticated_client):
    """Test a protected view that requires authentication."""
    response = authenticated_client.get("/profile/")
    assert response.status_code == 200
    assert "Profile" in str(response.content)
```

### Testing Django REST Framework

Test DRF APIs:

```python
@pytest.mark.django_db
@pytest.mark.api
def test_api_list(api_client):
    """Test listing objects via API."""
    # Create some test objects
    from myapp.models import Product
    Product.objects.create(name="Product 1", price=10.99)
    Product.objects.create(name="Product 2", price=20.99)
    
    # Test the API
    response = api_client.get("/api/products/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Product 1"
    assert data[1]["name"] == "Product 2"

@pytest.mark.django_db
@pytest.mark.api
def test_api_create(api_client):
    """Test creating an object via API."""
    response = api_client.post("/api/products/", {
        "name": "New Product",
        "price": 15.99,
        "description": "Created via API"
    }, format="json")
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Product"
    
    # Verify it was created in the database
    from myapp.models import Product
    product = Product.objects.get(id=data["id"])
    assert product.name == "New Product"
    assert product.price == 15.99
```

### Form Tests

Test Django forms:

```python
@pytest.mark.forms
def test_contact_form():
    """Test the contact form validation."""
    from myapp.forms import ContactForm
    
    # Test valid data
    form = ContactForm(data={
        "name": "John Doe",
        "email": "john@example.com",
        "message": "This is a test message"
    })
    assert form.is_valid()
    
    # Test invalid data
    form = ContactForm(data={
        "name": "John Doe",
        "email": "invalid-email",  # Invalid email
        "message": ""  # Empty message
    })
    assert not form.is_valid()
    assert "email" in form.errors
    assert "message" in form.errors
```

### URL Tests

Test URL configurations:

```python
@pytest.mark.urls
def test_url_patterns(client):
    """Test URL patterns and routing."""
    # Test that URLs resolve to the correct views
    from django.urls import reverse
    
    # Test a named URL
    url = reverse("home")
    assert url == "/"
    
    # Test a URL with parameters
    url = reverse("product-detail", kwargs={"pk": 1})
    assert url == "/products/1/"
```

### Admin Tests

Test Django admin:

```python
@pytest.mark.django_db
def test_admin_access(admin_client):
    """Test admin site access."""
    # admin_client is provided by pytest-django
    response = admin_client.get("/admin/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_model_admin(admin_client):
    """Test a model admin page."""
    # Create a test object
    from myapp.models import Product
    product = Product.objects.create(name="Admin Test", price=99.99)
    
    # Test the admin change list
    response = admin_client.get("/admin/myapp/product/")
    assert response.status_code == 200
    assert "Admin Test" in str(response.content)
    
    # Test the admin edit page
    response = admin_client.get(f"/admin/myapp/product/{product.id}/change/")
    assert response.status_code == 200
```

## Advanced Django Testing

### Custom Settings

Configure custom settings for tests:

```python
@pytest.mark.django_db
def test_with_custom_settings(settings):
    """Test with custom Django settings."""
    # Modify settings for this test
    settings.DEBUG = True
    settings.TEMPLATE_DEBUG = True
    
    # Test code that depends on these settings
    from django.conf import settings as django_settings
    assert django_settings.DEBUG is True
```

### Testing Middleware

Test Django middleware:

```python
@pytest.mark.django_db
def test_middleware(client):
    """Test middleware functionality."""
    # Assuming you have a custom security middleware that adds headers
    response = client.get("/")
    assert response.status_code == 200
    assert "X-Frame-Options" in response.headers
    assert response.headers["X-Frame-Options"] == "DENY"
```

### Testing Signals

Test Django signals:

```python
@pytest.mark.django_db
def test_signals():
    """Test that signals are fired correctly."""
    # Set up a signal receiver
    from django.db.models.signals import post_save
    from myapp.models import Product
    
    signal_received = False
    
    def signal_handler(sender, instance, created, **kwargs):
        nonlocal signal_received
        signal_received = True
        assert created is True
        assert instance.name == "Signal Test"
    
    # Connect the signal
    post_save.connect(signal_handler, sender=Product)
    
    try:
        # Trigger the signal
        Product.objects.create(name="Signal Test", price=50.00)
        
        # Check that the signal was received
        assert signal_received is True
    finally:
        # Disconnect the signal
        post_save.disconnect(signal_handler, sender=Product)
```

### Testing Templates

Test template rendering:

```python
@pytest.mark.django_db
def test_template_rendering(client):
    """Test that templates render correctly."""
    response = client.get("/")
    assert response.status_code == 200
    
    # Check template used
    assert "home.html" in [t.name for t in response.templates]
    
    # Check context
    assert "title" in response.context
    assert response.context["title"] == "Home"
    
    # Check content
    assert "Welcome to our site" in str(response.content)
```

## Running Django Tests

Using the Lightwave Testing Tools, you can run Django tests in various ways:

### Basic Test Running

```bash
# Run all Django tests
lightwave-dev test run

# Run with verbose output
lightwave-dev test run --verbose
```

### Test Selection

```bash
# Run model tests only
lightwave-dev test run --marker models

# Run view tests only
lightwave-dev test run --marker views

# Run API tests with database access
lightwave-dev test run --marker "api and django_db"

# Run tests in a specific file
lightwave-dev test run tests/test_models.py
```

### Coverage and Reports

```bash
# Run with coverage
lightwave-dev test run --coverage

# Generate HTML coverage report
lightwave-dev test run --coverage --cov-report html

# Generate multiple report types
lightwave-dev test run --coverage --cov-report "term,html,xml"
```

### Parallel Testing

```bash
# Run tests in parallel
lightwave-dev test run --parallel

# Specify number of processes
lightwave-dev test run --parallel --processes 4
```

## Using TDD with Django

Lightwave Testing Tools support Test-Driven Development for Django:

```bash
# Watch for changes and run tests automatically
lightwave-dev test tdd tests/test_models.py

# Watch with custom command
lightwave-dev test tdd tests/ --command "pytest {file} --ds=myproject.settings.test"
```

## Integration with Django Extensions

The testing tools work well with Django extensions:

### Django Debug Toolbar

```python
@pytest.fixture
def debug_toolbar_client(client, settings):
    """Return a client with Django Debug Toolbar enabled."""
    settings.INSTALLED_APPS += ["debug_toolbar"]
    settings.MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    settings.INTERNAL_IPS = ["127.0.0.1"]
    settings.DEBUG = True
    return client

@pytest.mark.django_db
def test_with_debug_toolbar(debug_toolbar_client):
    """Test with Django Debug Toolbar enabled."""
    response = debug_toolbar_client.get("/")
    assert response.status_code == 200
    # Debug toolbar will be visible in HTML
    assert "djDebug" in str(response.content)
```

### Django Channels

```python
@pytest.mark.asyncio
async def test_websocket_consumer():
    """Test a Django Channels WebSocket consumer."""
    from channels.testing import WebsocketCommunicator
    from myapp.consumers import MyConsumer
    
    # Connect to the consumer
    communicator = WebsocketCommunicator(MyConsumer.as_asgi(), "/ws/test/")
    connected, _ = await communicator.connect()
    assert connected
    
    # Test sending and receiving messages
    await communicator.send_json_to({"message": "hello"})
    response = await communicator.receive_json_from()
    assert response == {"message": "hello", "response": "world"}
    
    # Close the connection
    await communicator.disconnect()
```

## Best Practices for Django Testing

1. **Use appropriate markers**: Categorize your tests for better organization

2. **Test models thoroughly**: Cover validation, methods, and signals

3. **Separate unit and integration tests**: Unit tests should be fast and focused

4. **Use fixtures for common setup**: Create reusable fixtures in conftest.py

5. **Test forms and validation**: Ensure forms validate properly

6. **Test permission checks**: Verify authorization controls

7. **Mock external services**: Use pytest-mock for external APIs

8. **Keep tests isolated**: Tests should not depend on each other

## Conclusion

Testing Django applications with Lightwave Testing Tools provides a streamlined workflow for ensuring your web applications behave as expected. By leveraging the specialized fixtures, markers, and utilities provided by the tools, you can build robust test suites that validate your Django application's behavior thoroughly.

Remember to use the database fixtures properly, take advantage of Django-specific features like the `settings` fixture, and make use of the various test selection and reporting options to make your testing process efficient and effective. 