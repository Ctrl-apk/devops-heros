import pytest
import os
import tempfile

# Force test database URL before importing app
db_fd, db_path = tempfile.mkstemp(suffix=".db")
os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    try:
        os.close(db_fd)
        if os.path.exists(db_path):
            os.remove(db_path)
    except OSError:
        pass

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
