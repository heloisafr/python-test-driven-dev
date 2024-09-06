import os
import pytest
import rootpath
from api import app
from fastapi.testclient import TestClient

ROOT_DIR = rootpath.detect()


@pytest.fixture
def client():
    client = TestClient(app)
    yield client


@pytest.fixture
def test_folder():
    yield os.path.join(ROOT_DIR, "tests", "_resources")
