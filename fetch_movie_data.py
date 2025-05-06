import requests
from dotenv import load_dotenv
import os

load_dotenv()
APIKEY = os.getenv("APIKEY")


def fetching_movie_data(title):
    """getting year, rating and poster from the official
    omb api according to the title input from the user"""
    url = f"http://www.omdbapi.com/?apikey={APIKEY}&t={title}"
    res = requests.get(url)
    if res.status_code != 200:
        return "Failed to retrieve data from the API. Please try again later."
    movie_data = res.json()

    if movie_data.get("Response") == "False":
        return "Movie not found. Please try again with a different title."
    try:
        title_from_api = movie_data.get("Title")
        year = movie_data.get("Year", "No year available")
        ratings = movie_data.get("Ratings", 0)
        director = movie_data.get("Director", None)
        imdb_id = movie_data.get("imdbID", "")
        imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
        imdb_rating = 0
        for rating in ratings:
            if rating["Source"] == "Internet Movie Database":
                value = rating["Value"]
                imdb_rating = float(value.split("/")[0])
                break
        poster_url = movie_data.get("Poster", "")
        if not poster_url or poster_url == "N/A":
            poster_url = "https://s2.qwant.com/thumbr/474x711/4/8/40532943d13fbdaf8ca7370a42729118071213994e016b1df5e0ba0c475ec6/th.jpg?u=https%3A%2F%2Ftse.mm.bing.net%2Fth%3Fid%3DOIP.rQdMu0zwytqjkxEA5wZUAwHaLH%26pid%3DApi&q=0&b=1&p=0&a=0"
    except KeyError:
        return "Error: Missing information in the response data. Please try again."
    return title_from_api, year, imdb_rating, director, imdb_url, poster_url

