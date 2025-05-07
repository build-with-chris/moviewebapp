from models import db, User, Movie
from data_manager_interface import DataManagerInterface

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, app):
        db.init_app(app)
        self.db = db

    def get_all_users(self):
        return User.query.all()

    def get_user(self, user_id):
        return User.query.get(user_id)

    def get_movie(self, movie_id):
        return Movie.query.get(movie_id)

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_user(self, name):
        user = User(user_name=name)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def add_movie(self, user_id, title, year, rating, director, imdb_url, poster_url):
        new_movie = Movie(
            movie_name=title,
            movie_year=year,
            movie_rating=rating,
            movie_director=director,
            imdb_url=imdb_url,
            poster_url=poster_url,
            user_id=user_id

        )
        self.db.session.add(new_movie)
        self.db.session.commit()
        return new_movie

    def update_movie(self, movie_id, movie_data):
        movie=Movie.query.get(movie_id)
        if movie:
            movie.movie_name = movie_data.get('name', movie.movie_name)
            movie.movie_director = movie_data.get('director', movie.movie_director)
            movie.movie_year = movie_data.get('year', movie.movie_year)
            movie.movie_rating = movie_data.get('rating', movie.movie_rating)
            self.db.session.commit()
        return movie

    def delete_movie(self, movie_id):
        movie=Movie.query.get(movie_id)
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()
