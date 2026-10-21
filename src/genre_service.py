import hashlib
import json
import logging
import os

import requests
from dotenv import load_dotenv

from src.database.cache import cache_get, cache_set

load_dotenv()

logger = logging.getLogger(__name__)

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Cache durations
SEARCH_TTL = 600          # 10 minutes
MOVIE_DETAILS_TTL = 3600  # 1 hour

# Avoid waiting indefinitely for TMDB
REQUEST_TIMEOUT = 10


def _cache_key(prefix: str, params: dict) -> str:
    """Generate a stable cache key from request parameters."""
    serialized = json.dumps(
        params,
        sort_keys=True,
        ensure_ascii=False,
    )

    digest = hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()

    return f"movie_agent:tmdb:{prefix}:{digest}"


def search_movie(movie_name):
    """
    Search TMDB for a movie.
    Returns the complete JSON response or None on failure.
    """

    if not TMDB_API_KEY:
        logger.error("TMDB_API_KEY is not configured")
        return None

    query = str(movie_name).strip()

    if not query:
        return None

    key = _cache_key(
        "search",
        {"query": query.casefold()},
    )

    # 1. Check Redis
    cached = cache_get(key)

    if cached is not None:
        return cached

    # 2. Request TMDB
    url = f"{TMDB_BASE_URL}/search/movie"

    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()

    except (requests.RequestException, ValueError):
        logger.warning(
            "TMDB movie search failed",
            exc_info=True,
        )
        return None

    # Cache only successful responses
    if isinstance(data, dict) and "results" in data:
        cache_set(key, data, ttl=SEARCH_TTL)

    return data


def get_movie_id(movie_name):
    """
    Return the TMDB ID of the first matching movie.
    """

    data = search_movie(movie_name)

    if data is None:
        return None

    results = data.get("results", [])

    if not results:
        return None

    return results[0].get("id")


def get_movie_details(movie_name):
    """
    Return complete TMDB movie details.
    Returns None if the movie cannot be found or the request fails.
    """

    if not TMDB_API_KEY:
        logger.error("TMDB_API_KEY is not configured")
        return None

    query = str(movie_name).strip()

    if not query:
        return None

    key = _cache_key(
        "details",
        {"movie_name": query.casefold()},
    )

    # 1. Check Redis for previously fetched details
    cached = cache_get(key)

    if cached is not None:
        return cached

    # 2. Find the TMDB movie ID
    movie_id = get_movie_id(query)

    if movie_id is None:
        return None

    # 3. Fetch full movie details
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"

    params = {
        "api_key": TMDB_API_KEY,
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()

    except (requests.RequestException, ValueError):
        logger.warning(
            "TMDB movie details request failed",
            exc_info=True,
        )
        return None

    # Cache successful detail responses only
    if isinstance(data, dict) and data.get("id") is not None:
        cache_set(key, data, ttl=MOVIE_DETAILS_TTL)

    return data


def get_movie_genres(movie_name):
    """
    Return the genre names for a movie.
    Reuses the cached movie-details response.
    """

    details = get_movie_details(movie_name)

    if details is None:
        return []

    return [
        genre["name"]
        for genre in details.get("genres", [])
        if isinstance(genre, dict) and "name" in genre
    ]


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

    if details:
        print(details.get("title"))
        print(details.get("release_date"))
        print(details.get("vote_average"))
        print(details.get("genres"))
    else:
        print("Movie details unavailable")

# communicates with TMDB