# tests/conftest.py
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from database import get_session
from authentic.dependencies import get_current_user
from models import User

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"  

# Async engine for tests
test_engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)

# Session factory for tests
TestSessionLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def override_get_session():
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

async def override_get_current_user():
    """Fake logged-in user for testing."""
    return User(id=1, username="testuser", password_hash="fakehash")

app.dependency_overrides[get_current_user] = override_get_current_user

@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_test_db():
    """Create tables before tests, drop after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac