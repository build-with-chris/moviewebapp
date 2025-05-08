from flask import Flask, render_template, request, flash, url_for
import os

from flask.cli import load_dotenv
from werkzeug.utils import redirect
from datamanager import SQLiteDataManager
from models import db, User, Movie
import fetch_movie_data
import dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.secret_key = SECRET_KEY

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'moviewebapp.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
data_manager = SQLiteDataManager(app)


@app.route('/')
def home():
    """the startpage will be to select your name or add it in the nav bar.
    In future there could be a home html"""
    return redirect(url_for('list_users'))


@app.route('/users')
def list_users():
    """display all users"""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/all_movies')
def all_movies():
    """display all movies + their ratings + user_name"""
    movies = Movie.query.all()
    return render_template('all_movies.html', movies=movies)

@app.route('/users/<int:user_id>', methods=["GET", "POST"])
def list_user_movies(user_id):
    """the heart of the flask app. shows the movies a user has saved"""
    user = data_manager.get_user(user_id)
    movies = data_manager.get_user_movies(user_id)
    if not user:
        flash("User is not in the database yet")
        return redirect(url_for('list_users'))
    return render_template('user_movies.html', user=user, movies=movies)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """adding a user by receiving his/her name"""
    if request.method=='POST':
        name = request.form['name']
        try:
            user=data_manager.add_user(name)
            flash(f'User {user.user_name} was successfully added.')
        except Exception as e:
            flash("Could not save the user.")
            print("DB Error:", e)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=["GET", "POST"])
def add_movie(user_id):
    """adding a movie by inserting a title. The rest is done by oMDb Api
    if no title was found it flashes a message and redirects you to user_movies"""
    user=data_manager.get_user(user_id)
    if request.method == 'POST':
        title = request.form['title']

        values = fetch_movie_data.fetching_movie_data(title)

        if isinstance(values, str):
            flash(values)
            return redirect(url_for('list_user_movies', user_id=user_id))

        title_from_api, year, rating, director, poster, imdb_url = values
        try:
            data_manager.add_movie(user_id, title_from_api, year, rating, director, poster, imdb_url)
            flash(f'Movie "{title_from_api}" was successfully added.')
            return redirect(url_for('list_user_movies', user_id=user_id))
        except Exception as e:
            flash("Could not save the movie.")
            print("DB Error:", e)

    return render_template('add_movie.html', user=user)


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    """overwriting the pre given values from the Api"""
    movie = data_manager.get_movie(movie_id)
    if  not movie:
        flash("Movie is not in the database yet")
        return redirect(url_for('list_user_movies', user_id=user_id))
    if request.method =='POST':
        updated_details = {
            "name" : request.form["name"],
            "director" : request.form["director"],
            "year" : request.form["year"],
            "rating" : request.form["rating"]
        }
        try:
            data_manager.update_movie(movie_id, updated_details)
            flash("Movie is updated")
            return redirect(url_for('list_user_movies', user_id=user_id))
        except Exception as e:
            flash("Could not update the movie.")
            print("Error:", e)

    return render_template("update_movie.html", movie=movie, user_id=user_id)


@app.route('/update_user/<int:user_id>', methods=["GET", "POST"])
def update_user(user_id):
    """change the username"""
    user= data_manager.get_user(user_id)
    if request.method == "POST":
        new_name = {
            "name": request.form["name"]
        }
        data_manager.update_user(user_id, new_name)

        flash("Username updated")
        return redirect(url_for('list_user_movies', user_id=user_id))
    return render_template("update_user.html", user=user)


@app.route('/users/<user_id>/delete_movie/<movie_id>', methods=["POST"])
def delete_movie(user_id, movie_id):
    movie = data_manager.get_movie(movie_id)
    if request.method == 'POST':
        data_manager.delete_movie(movie_id)
        flash(f'Movie {movie.movie_name} was successfully deleted.')
        return redirect(url_for(f'list_user_movies', user_id=user_id))


@app.route('/delete_user/<user_id>', methods=["POST"])
def delete_user(user_id):
    """deletes the user AND all the movies within the list_user_movies
    for more details look on the dependencies in models"""
    user = data_manager.get_user(user_id)
    if user:
        data_manager.delete_user(user_id)
        flash(f'User {user.user_name} was successfully deleted.')
    return redirect(url_for(f'list_users'))


#simple error handling that redirects to a template
@app.errorhandler(404)
def page_not_found(e):
    if request.method =="POST":
        return redirect(url_for('list_users'))
    return render_template('404.html'), 404

@app.errorhandler(405)
def method_not_allowed(error):
    if request.method =="POST":
        return redirect(url_for('list_users'))
    return render_template('404.html'), 405

@app.errorhandler(500)
def internal_server_error(error):
    print("💥 500 Error:", error)  # Optional logging
    return render_template('500.html'), 500

@app.errorhandler(Exception)
def all_exception_handler(error):
    print("💥 Unhandled Exception:", error)
    return render_template("500.html"), 500


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)