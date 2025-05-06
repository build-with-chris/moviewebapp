from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)

    def __repr__(self):
        return f"User(id = {self.user_id}, name = {self.user_name})"


class Movie(db.Model):
    __tablename__ = 'movies'

    movie_id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String)
    movie_director = db.Column(db.String)
    movie_year = db.Column(db.Integer)
    movie_rating = db.Column(db.Float)
    poster_url = db.Column(db.String)
    imdb_url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))



