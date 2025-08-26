# Testing Guide for SwatchWorx API

This guide explains how to run tests for the SwatchWorx FastAPI application.

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Project structure**:
   ```
   /workspaces/swatchworx-app/
   ├── main.py              # FastAPI application
   ├── models.py            # Pydantic models
   ├── data.py             # Test data
   ├── requirements.txt    # Dependencies including pytest
   ├── pytest.ini         # Pytest configuration
   └── tests/              # Test directory
       ├── __init__.py
       ├── conftest.py     # Shared fixtures
       ├── test_main.py    # Main API endpoint tests
       └── test_integration.py # Integration & async tests
   ```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run tests with verbose output:
```bash
pytest -v
```

### Run specific test file:
```bash
pytest tests/test_main.py
pytest tests/test_integration.py
```

### Run specific test class or method:
```bash
pytest tests/test_main.py::TestRootEndpoint
pytest tests/test_main.py::TestGetSwatchConfigEndpoint::test_get_all_swatches_without_filter
```

### Run tests matching a pattern:
```bash
pytest -k "swatch"
pytest -k "async"
```

## Test Coverage

### Main API Tests (`test_main.py`):
- **Root endpoint (`/`)**: Basic API info and content type
- **Get swatch config endpoint (`/get_swatch_config`)**:
  - Get all swatches (no filter)
  - Filter by valid colornames
  - Filter by invalid colornames (404 errors)
  - Empty colorname handling
  - Case sensitivity
  - Response schema validation
  - Data integrity checks
- **Edge cases**: Wrong HTTP methods, non-existent endpoints
- **Data consistency**: Enum validation, color value format
- **Parameterized tests**: Multiple valid/invalid colornames

### Integration Tests (`test_integration.py`):
- **Async endpoints**: All endpoints tested with async HTTP client
- **Workflow scenarios**: Complete API usage workflows
- **Concurrent requests**: Thread safety testing
- **Performance**: Basic response time and load testing

## Test Fixtures

Shared fixtures in `conftest.py`:
- `client()`: Synchronous test client for FastAPI app
- `sample_colornames()`: Valid colornames for testing
- `invalid_colornames()`: Invalid colornames for error testing

## Sample Output

When tests pass, you'll see:
```
====================== 29 passed, 1 warning in 0.13s ======================
```

When tests fail, pytest shows detailed error information to help debug issues.

## Writing New Tests

1. Add new test methods to existing test classes
2. Create new test classes for new functionality
3. Use the shared fixtures from `conftest.py`
4. Follow the naming convention: `test_*`
5. Use descriptive docstrings for test methods

## Common Test Commands

```bash
# Run all tests
pytest

# Run with coverage (if coverage is installed)
pytest --cov=.

# Run tests and stop at first failure
pytest -x

# Run tests in parallel (if pytest-xdist is installed)
pytest -n auto

# Run only failed tests from last run
pytest --lf
```
