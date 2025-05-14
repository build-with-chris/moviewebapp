import requests
import re
import logging
import os

from dotenv import load_dotenv

# Configure module-level logger
debug_logger = logging.getLogger(__name__)
debug_logger.setLevel(logging.INFO)

# Load environment variables
load_dotenv()
APIKEY = os.getenv("APIKEY")


def fetching_movie_data(title):
    """Fetch year, IMDb rating, director, link, and poster from OMDB API for a given title."""
    # Validate API key
    url = f"http://www.omdbapi.com/?apikey={APIKEY}&t={title}"
    debug_logger.info(f"OMDB Request URL: {url}")

    try:
        res = requests.get(url, timeout=10)
        debug_logger.info(f"OMDB Response Code: {res.status_code}")
    except requests.RequestException as e:
        debug_logger.exception("OMDB request failed")
        return "Failed to retrieve data from the API. Please try again later."

    if res.status_code != 200:
        debug_logger.error(f"Non-200 response from OMDB: {res.status_code}")
        return "Failed to retrieve data from the API. Please try again later."

    try:
        movie_data = res.json()
        debug_logger.info(f"API Response Data: {movie_data}")
    except ValueError:
        debug_logger.error(f"Invalid JSON received: {res.text}")
        return "Error parsing API response. Please try again later."

    if movie_data.get("Response") == "False":
        error_msg = movie_data.get("Error", "Movie not found. Please try again.")
        debug_logger.warning(f"OMDB Error Response: {error_msg}")
        return error_msg

    try:
        title_from_api = movie_data.get("Title")
        year_raw = movie_data.get("Year", "")
        year_match = re.search(r"\d{4}", year_raw)
        year = int(year_match.group()) if year_match else None

        ratings = movie_data.get("Ratings", [])
        director = movie_data.get("Director")
        imdb_id = movie_data.get("imdbID", "")
        imdb_url = f"https://www.imdb.com/title/{imdb_id}/" if imdb_id else None

        imdb_rating = 0.0
        for rating in ratings:
            if rating.get("Source") == "Internet Movie Database":
                try:
                    imdb_rating = float(rating.get("Value").split("/")[0])
                except Exception:
                    imdb_rating = 0.0
                break

        poster_url = movie_data.get("Poster")
        if not poster_url or poster_url == "N/A":
            poster_url = (
                "https://s2.qwant.com/thumbr/474x711/4/8/"
                "40532943d13fbdaf8ca7370a42729118071213994e016b1df5e0ba0c475ec6/"
                "th.jpg?u=https%3A%2F%2Ftse.mm.bing.net%2Fth%3Fid%3DOIP.rQdMu0zwytqjkxEA5wZUAwHaLH%26pid%3DApi"
            )

    except Exception as e:
        debug_logger.exception("Error processing OMDB data")
        return "Error processing API data. Please try again later."

    return title_from_api, year, imdb_rating, director, poster_url, imdb_url
