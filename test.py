from flask import Flask
from datamanager import SQLiteDataManager
from models import db, User
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'test.sqlite')

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'

with app.app_context():
    manager=SQLiteDataManager(app)
    db.drop_all()
    db.create_all()

    user = User(user_name="Alice")
    db.session.add(user)
    db.session.commit()

    manager.add_movie(user.user_id, {
        "name" : "Mokeys",
        "director" : "Mathias Eder",
        "year" : 2023,
        "rating" : 7.0
    })

    movies = manager.get_user_movies(user.user_id)
    for movie in movies:
        print(f'{movie.movie_name}, {movie.movie_year} – Rating: {movie.movie_rating}')
