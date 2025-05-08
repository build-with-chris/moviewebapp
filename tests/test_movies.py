import pytest
from app import app, db
from models import User, Movie
from unittest.mock import patch


@pytest.fixture
def client():
    """default decorator for Testing purposes"""
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


@patch('fetch_movie_data.fetching_movie_data')
def test_update_movie(mock_fetch, client):
    """test if updated values appear in the db. For simple purposes we use a patcher"""
    mock_fetch.return_value = (
        "Papa", 2022, 7.5, "John Doe", "https://example.com", "https://imdb.com/title/tt123"
    )

    response = client.post("/add_user", data={"name": "Testuser"}, follow_redirects=True)

    user = User.query.filter_by(user_name="Testuser").first()

    response = client.post(f"/users/{user.user_id}/add_movie",
                           data = {"title": "Papa"}, follow_redirects=True)
    movie = Movie.query.filter_by(movie_name="Papa").first()

    response = client.post(
        f"/users/{user.user_id}/update_movie/{movie.movie_id}",
        data={"name": "Papa", "year": 2022, "rating": 10.0, "director": "John Doe"},
        follow_redirects=True
    )

    movie = Movie.query.get(movie.movie_id)

    assert response.status_code == 200
    assert movie.movie_rating == 10


def test_delete_movie(client):
    response = client.post("/add_user", data={"name": "old"}, follow_redirects=True)
    user = User.query.filter_by(user_name="old").first()

    response = client.post(f"/users/{user.user_id}/add_movie",
                           data={"title": "Papa"}, follow_redirects=True)
    movie = Movie.query.filter_by(movie_name="Papa").first()


    response = client.post(f'/users/{user.user_id}/delete_movie/{movie.movie_id}', follow_redirects=True)
    assert response.status_code == 200

    deleted_movie = Movie.query.get(movie.movie_id)
    assert deleted_movie is None