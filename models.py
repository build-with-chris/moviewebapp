from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """setting up a simple User, that has a required name and is in relation to his/her movies
    if a user gets deleted, it will also delete all the movies within the user"""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    movies = db.relationship('Movie', backref='user', cascade='all, delete', lazy=True)

    def __repr__(self):
        return f"User(id = {self.user_id}, name = {self.user_name})"


class Movie(db.Model):
    """the Movie class has various attributes, connected to a user_id"""
    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String)
    movie_director = db.Column(db.String)
    movie_year = db.Column(db.Integer)
    movie_rating = db.Column(db.Float)
    poster_url = db.Column(db.String)
    imdb_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    reviews = db.relationship('Review', backref='movie', cascade="all, delete-orphan")


class Review(db.Model):
    __tablename__ = 'reviews'

    review_id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.String)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'))

