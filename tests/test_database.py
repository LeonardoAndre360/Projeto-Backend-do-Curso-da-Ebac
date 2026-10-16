import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import Base, LivroDB, app
from fastapi.testclient import TestClient
import os

DATABASE_URL_TEST = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL_TEST, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_redis(mocker):
    mock_redis_client = mocker.patch("main.redis_client", autospec=True)
    mock_redis_client.get.return_value = None

@pytest.fixture(scope="function")
def db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_get_books(db, mocker):
    response = client.get("/livros", auth=("admin", "admin"))
    assert response.status_code == 200

    data = response.json()

    assert len(data["Livros"]) == 7
    assert data["Livros"][0]["nome_livro"] == "Harry Potter e a O Calise de fogo"
    assert data["Livros"][0]["autor_livro"] == "J. K. Rowling"
    assert data["Livros"][0]["ano_livro"] == 1997