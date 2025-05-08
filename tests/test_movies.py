import pytest
from app import app, db
from models import User, Movie


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_add_movie(client):
    response = client.post("/add_user", data={"name": "Testuser"}, follow_redirects=True)

    user = User.query.filter_by(user_name="Testuser").first()

    response = client.post(f"/users/{user.user_id}/add_movie",
                           data = {"title": "Papa"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Papa" in response.data



