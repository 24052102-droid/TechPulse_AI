import os
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Force local sqlite and in-memory cache for CI tests
os.environ["DATABASE_URL"] = "sqlite:///./test_ci.db"
os.environ["REDIS_URL"] = "redis://localhost:6379/9"
os.environ["ENVIRONMENT"] = "testing"
os.environ["DEBUG"] = "False"

from backend.app.core.database import init_db, engine, Base
from backend.app.main import app
from backend.app.ml.inference import ml_engine


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_db()
    if not ml_engine.is_loaded:
        ml_engine.load_models()
    yield
    # Teardown
    Base.metadata.drop_all(bind=engine)
    if os.path.exists("./test_ci.db"):
        try:
            os.remove("./test_ci.db")
        except OSError:
            pass


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
