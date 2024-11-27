import pytest
from api.v1.app import app
from models import storage
from tests.utils import setup_test_db, clear_test_db

@pytest.fixture
def client():
    """Test client fixture"""
    return app.test_client()

@pytest.fixture
def test_data():
    """Test data fixture"""
    data = setup_test_db()
    yield data
    clear_test_db()

@pytest.fixture
def headers():
    """Headers fixture"""
    return {'Content-Type': 'application/json'}