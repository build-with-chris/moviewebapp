from models import db, User, Movie
from data_manager_interface import DataManagerInterface

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        db.init_app(app)
        self.db = db

    def get_all_users(self):
        return User.query.all()

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, user_id, movie_data):
        new_movie = Movie(
            movie_name = movie_data['name'],
            movie_director=movie_data['director'],
            movie_year=movie_data['year'],
            movie_rating=movie_data['rating'],
            user_id=user_id
        )
        self.db.session.add(new_movie)
        self.db.session.commit()

    def update_movie(self, movie_id, movie_data):
        movie=Movie.query.get(movie_id)
        if movie:
            movie.movie_name = movie_data.get(movie_data['name'], movie.movie_name),
            movie.movie_director = movie_data.get(movie_data['director'], movie.movie_director)
            movie.movie_year = movie_data.get(movie_data['year'], movie.movie_year),
            movie.movie_rating = movie_data.get(movie_data['rating'], movie.movie_rating)
            self.db.session.commit()

    def delete_movie(self, movie_id):
        movie=Movie.query.get(movie_id)
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()
