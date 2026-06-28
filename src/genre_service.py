import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")


def search_movie(movie_name):
    """
    Search for a movie on TMDB. Returns the complete JSON response.
    """

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "query": movie_name
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    return response.json()


def get_movie_id(movie_name):
    """
    Returns the TMDB movie ID.
    """

    data = search_movie(movie_name)

    if data is None:
        return None

    results = data.get("results", [])

    if len(results) == 0:
        return None

    return results[0]["id"]


def get_movie_details(movie_name):
    """
    Returns complete movie details from TMDB.
    """

    movie_id = get_movie_id(movie_name)

    if movie_id is None:
        return None

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": TMDB_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    return response.json()


def get_movie_genres(movie_name):
    """
    Returns only the genre names.
    """

    details = get_movie_details(movie_name)

    if details is None:
        return []

    genres = []

    for genre in details.get("genres", []):
        genres.append(genre["name"])

    return genres


if __name__ == "__main__":

    movie = "Interstellar"

    print("=" * 50)

    print("Movie ID:")
    print(get_movie_id(movie))

    print("=" * 50)

    print("Genres:")
    print(get_movie_genres(movie))

    print("=" * 50)

    print("Movie Details:")
    details = get_movie_details(movie)

    print(details["title"])
    print(details["release_date"])
    print(details["vote_average"])
    print(details["genres"])

# communicates with TMDB