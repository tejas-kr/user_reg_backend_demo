import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from ..main import app
from ..utils.db_utils import get_session
from ..utils.auth_utils import get_current_user
from ..models.token import Token, TokenData
from ..models.users import (
    User, UserLogin, UserBase, UserCreate, UserPass,
)


test_engine = create_engine("sqlite:///:memory:", echo=True)


def get_test_session():
    """
    :yield: DB Session
    """
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_session] = get_test_session


async def mock_get_current_user():
    return {"email": "test_user@test.test"}


app.dependency_overrides[get_current_user] = mock_get_current_user


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        user = User(email="test_user@test.test", password="TestPass&&rd123", full_name="Test User")
        session.add(user)
        session.commit()


client = TestClient(app)


def test_get_book_by_id():
    test_book_id: int = 2
    response = client.get(f"/book/{test_book_id}", headers={"Authorization": "Bearer test_token1243^&5"})
    assert response.status_code == 200
    assert response.json() == {"message": "working"}
