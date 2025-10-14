"""
Pytest configuration and shared fixtures for ScriPTA tests.
"""

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from ..main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest_asyncio.fixture
async def async_client():
    """Create an async test client for the FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_colornames():
    """Provide sample colornames for testing."""
    return ["DIELINE", "PA123", "PA321"]


@pytest.fixture
def invalid_colornames():
    """Provide invalid colornames for testing."""
    return ["NONEXISTENT", "INVALID", "NOT_FOUND", "", "lowercase"]


@pytest.fixture
def sample_config_names():
    """Provide sample config names for testing."""
    return ["default", "FoldingBox", "Label", "TPM"]


@pytest.fixture
def invalid_config_names():
    """Provide invalid config names for testing."""
    return ["NONEXISTENT", "INVALID", "NOT_FOUND", "DEFAULT", "foldingbox"]
