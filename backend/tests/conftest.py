"""
Pytest configuration and shared fixtures for ScriPTA tests.
"""

import pytest
from fastapi.testclient import TestClient

from ..main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


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
