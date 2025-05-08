import pytest
from app import app, db
from models import User


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_add_user(client):
    response = client.post("/add_user", data={"name": "Testuser"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Testuser" in response.data

def test_edit_name(client):
    response = client.post("/add_user", data={"name": "Old"}, follow_redirects=True)
    user = User.query.filter_by(user_name="Old").first()

    response = client.post(f'/update_user/{user.user_id}', data={"name": "New"}, follow_redirects=True)
    assert response.status_code == 200



def test_delete_user(client):
    response = client.post("/add_user", data={"name": "old"}, follow_redirects=True)
    user = User.query.filter_by(user_name="old").first()

    response = client.post(f'/delete_user/{user.user_id}', follow_redirects=True)
    assert response.status_code == 200

    deleted_user = User.query.get(user.user_id)
    assert deleted_user is None