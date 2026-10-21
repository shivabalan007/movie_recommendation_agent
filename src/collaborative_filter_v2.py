import hashlib
import json

import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from src.utils import clean_title
from src.database.cache import cache_get, cache_set


# LOAD SAVED MATRIX
movie_user_matrix = joblib.load(
    r"C:\Dev\projects\movie_recommendation_agent\data\models\movie_user_matrix.pkl"
)


# CACHE KEY
def _cache_key(prefix: str, params: dict) -> str:
    """Generate a stable Redis key from function inputs."""

    serialized = json.dumps(
        params,
        sort_keys=True,
        ensure_ascii=False,
    )

    digest = hashlib.sha256(
        serialized.encode("utf-8")
    ).hexdigest()

    return f"movie_agent:{prefix}:{digest}"

# FIND MOVIE TITLE

def find_movie_title(movie_name):

    movie_name = movie_name.lower().strip()

    for title in movie_user_matrix.index:

        clean = clean_title(title).lower()

        if clean == movie_name:
            return title

    return None


# COLLABORATIVE RECOMMENDATION
def recommend_cf_movies(movie_name, top_n=10):

    key = _cache_key(
        "collaborative",
        {
            "movie_name": str(movie_name).strip().casefold(),
            "top_n": top_n,
        },
    )

    # 1. Check Redis first
    cached = cache_get(key)

    if cached is not None:
        return cached

    # 2. Run the original recommendation logic
    movie_title = find_movie_title(movie_name)

    if movie_title is None:
        return []

    similarity_scores = cosine_similarity(
        movie_user_matrix.loc[[movie_title]],
        movie_user_matrix,
    )[0]

    similarity_series = pd.Series(
        similarity_scores,
        index=movie_user_matrix.index,
    )

    recommendations = similarity_series.sort_values(
        ascending=False
    ).iloc[1:top_n + 1]

    results = []

    for title, score in recommendations.items():

        results.append({
            "title": clean_title(title),
            "cf_score": round(float(score), 3),
        })

    # 3. Save result for 1 hour
    cache_set(key, results, ttl=3600)

    return results


# COLLABORATIVE MOVIE SEARCH
def search_movie(movie_name):

    key = _cache_key(
        "collaborative_search",
        {
            "movie_name": str(movie_name).strip().casefold(),
        },
    )

    # 1. Check Redis
    cached = cache_get(key)

    if cached is not None:
        return cached

    # 2. Run the original search logic
    movie_name = movie_name.lower()

    matches = []

    for title in movie_user_matrix.index:

        if movie_name in title.lower():
            matches.append(clean_title(title))

    results = matches[:20]

    # 3. Cache for 10 minutes
    cache_set(key, results, ttl=600)

    return results


# TEST
if __name__ == "__main__":

    movie_name = "Alien"

    print("\n========== COLLABORATIVE FILTER TEST ==========")

    print("\n--- First recommendation request ---")
    first = recommend_cf_movies(movie_name)
    print(first)

    print("\n--- Repeated recommendation request ---")
    second = recommend_cf_movies(movie_name)
    print(second)

    print("\n--- First search request ---")
    search_first = search_movie(movie_name)
    print(search_first)

    print("\n--- Repeated search request ---")
    search_second = search_movie(movie_name)
    print(search_second)

    assert first == second
    assert search_first == search_second

    print("\nAll functional tests passed.")

# Main objective is People who liked x also like y - People who liked similar movies also liked this.