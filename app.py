from flask import Flask, render_template, request
import os
from datamanager import SQLiteDataManager
from models import db, User

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'moviewebapp.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
data_manager = SQLiteDataManager(app)

@app.route('/')
def home():
    return "Welcome to MovieWeb App!"

@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/users/<user_id>')
def list_user_movies(user_id):
    pass

@app.route('/add_user')
def add_user():
    pass

@app.route('/users/<user_id>/add_movie')
def add_movie():
    pass


@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie(user_id, movie_id):
    pass

@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    pass


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)