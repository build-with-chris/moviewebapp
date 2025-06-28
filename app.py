
from flask import Flask, render_template, request, flash, url_for, send_from_directory
from werkzeug.utils import redirect

from AI import ask_movie_assistent
from datamanager import SQLiteDataManager
from models import db, Movie
import fetch_movie_data
from dotenv import load_dotenv
import os
from api import api, init_api
import sys
from config import DevelopmentConfig, ProductionConfig




load_dotenv()


app = Flask(__name__)
env = os.getenv('FLASK_ENV', 'development')
if env == 'production':
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)


data_manager = SQLiteDataManager(app)


init_api(data_manager)
app.register_blueprint(api, url_prefix='/api')


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
@app.route('/users/<int:user_id>/add_movie', methods=["GET", "POST"])
def add_movie(user_id):
    """adding a movie by inserting a title. The rest is done by OMDb API"""
    user = data_manager.get_user(user_id)
    app.logger.info(f"🛠️ Entered add_movie for user_id={user_id}, method={request.method}")
    if request.method == 'POST':
        title = request.form.get('title')
        if not title:
            app.logger.warning("No title provided in add_movie form!")
            flash("Bitte gib einen Filmtitel ein.")
            return redirect(url_for('add_movie', user_id=user_id))

        # Fetch movie data from OMDB
        result = fetch_movie_data.fetching_movie_data(title)
        if isinstance(result, str):
            app.logger.error(f"OMDB fetch error: {result}")
            flash(result)
            return redirect(url_for('list_user_movies', user_id=user_id))

        title_from_api, year, rating, director, poster_url, imdb_url = result
        try:
            new_movie = data_manager.add_movie(
                user_id, title_from_api, year, rating, director, poster_url, imdb_url
            )
            app.logger.info(f"✅ Movie added: {title_from_api}")
            flash(f'Film "{title_from_api}" wurde erfolgreich hinzugefügt.')
            return redirect(url_for('list_user_movies', user_id=user_id))
        except Exception as e:
            app.logger.exception("🔥 Fehler beim Speichern des neuen Films")
            flash("Konnte den Film nicht speichern.")
            return redirect(url_for('list_user_movies', user_id=user_id))

    # GET request: render the add form
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


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def update_user(user_id):
    user = data_manager.get_user(user_id)
    if request.method == "POST":
        # Debug-Log, um sicherzugehen, dass wir hier ankommen:
        print(f"🛠️ Entered POST update_user for id={user_id}", file=sys.stderr, flush=True)
        try:
            new_name = {
            "name": request.form["name"]
            }
            data_manager.update_user(user_id, new_name)
            flash("Username updated")
            return redirect(url_for('list_user_movies', user_id=user_id))
        except Exception as e:
            # Schiebe den vollständigen Traceback ins Error-Log
            app.logger.exception("🔥 Exception in update_user")
            # Zeige dem User wenigstens eine Fehlermeldung
            return render_template("update_user.html", user=user,
                                   error="Beim Speichern ist ein interner Fehler aufgetreten"), 500
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


@app.route('/users/<int:user_id>/add_review/<int:movie_id>', methods=["GET", "POST"])
def add_review(user_id, movie_id):
    movie = data_manager.get_movie(movie_id)
    if not movie:
        flash("Movie is not in the database yet")
        return redirect(url_for('list_user_movies', user_id=user_id, movie_id=movie_id))
    if request.method == 'POST':
        review_text = request.form["review"]
        data_manager.add_review(movie_id, review_text)
        flash("Review added")
        return redirect(url_for('list_user_movies', user_id=user_id))
    return render_template('add_review.html', movie=movie)


@app.route('/user/<int:user_id>/ask', methods=["POST"])
def chat_assistant(user_id):
    user_input=request.form["message"]
    reply = ask_movie_assistent(user_input)
    movies = data_manager.get_user_movies(user_id)
    user = data_manager.get_user(user_id)
    return render_template("user_movies.html", user=user, movies=movies, ai_reply=reply)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

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