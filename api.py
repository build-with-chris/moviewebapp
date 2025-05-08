from crypt import methods

from flask import Blueprint, jsonify
from models import Movie

api = Blueprint('api', __name__)
data_manager = None

def init_api(manager):
    global data_manager
    data_manager = manager

@api.route('/users', methods=['GET'])
def get_users():
    users = data_manager.get_all_users()
    users_dict = [{"user_id": u.user_id, "user_name": u.user_name} for u in users]
    return jsonify(users_dict)


@api.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movie_dict = [{"movie_id": m.movie_id, "movie_name": m.movie_name, "movie_year": m.movie_year, "movie_rating": m.movie_rating,
                   "poster_url": m.poster_url, "imdb_url": m.imdb_url, "user_id": m.user_id,
                   "reviews": [r.review_text for r in m.reviews]
                   } for m in movies]
    return jsonify(movie_dict)
