import hashlib
import json

import joblib
import pandas as pd

from src.database.cache import cache_get, cache_set


latest_movies = pd.read_csv(
    r"C:\Dev\projects\movie_recommendation_agent\data\processed\latest_movies_final.csv"
)

similarity_matrix = joblib.load(
    r"C:\Dev\projects\movie_recommendation_agent\data\embeddings\similarity_matrix.pkl"
)

# Movie title -> index mapping
movie_indices = pd.Series(
    latest_movies.index,
    index=latest_movies["title"]
).drop_duplicates()


def _cache_key(prefix: str, params: dict) -> str:
    """Create a stable key from function inputs."""
    serialized = json.dumps(
        params,
        sort_keys=True,
        ensure_ascii=False,
    )
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    return f"movie_agent:{prefix}:{digest}"


def recommend_semantic_movies(movie_name, num_recommendation=10):
    key = _cache_key(
        "semantic",
        {
            "movie_name": str(movie_name).strip().casefold(),
            "num_recommendation": num_recommendation,
        },
    )

    cached = cache_get(key)
    if cached is not None:
        return cached

    exact_match = None
    matches = []

    for title in movie_indices.index:
        if title.lower() == movie_name.lower():
            exact_match = title

        if movie_name.lower() in title.lower():
            matches.append(title)

    if exact_match:
        matched_movie = exact_match
    elif matches:
        matched_movie = matches[0]
    else:
        return []

    movie_index = movie_indices[matched_movie]

    similarity_scores = list(
        enumerate(similarity_matrix[movie_index])
    )

    similarity_scores.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    top_movies = similarity_scores[1:num_recommendation + 1]

    recommendations = []

    for movie in top_movies:
        row = latest_movies.iloc[movie[0]]

        recommendations.append({
            "title": row["title"],
            "rating": round(float(row["vote_average"]), 1),
            "year": str(row["release_date"])[:4],
            "similarity_score": round(float(movie[1]), 3),
        })

    cache_set(key, recommendations, ttl=3600)
    return recommendations


def search_movie(query):
    key = _cache_key(
        "search",
        {"query": str(query).strip().casefold()},
    )

    cached = cache_get(key)
    if cached is not None:
        return cached

    matches = []

    for title in latest_movies["title"]:
        if query.lower() in title.lower():
            matches.append(title)

    results = matches[:10]

    cache_set(key, results, ttl=600)
    return results


def get_movie_details(movie_name):
    key = _cache_key(
        "details",
        {"movie_name": str(movie_name).strip().casefold()},
    )

    cached = cache_get(key)
    if cached is not None:
        return cached

    movie = latest_movies[
        latest_movies["title"].str.lower() == movie_name.lower()
    ]

    if movie.empty:
        return None

    movie = movie.iloc[0]

    result = {
        "title": movie["title"],
        "overview": movie["overview"],
        "rating": round(float(movie["vote_average"]), 1),
        "release_year": str(movie["release_date"])[:4],
    }

    cache_set(key, result, ttl=3600)
    return result


if __name__ == "__main__":
    print("\n========== TESTING REDIS CACHE ==========")

    # 1. Movie details
    print("\n--- Movie Details ---")
    details = get_movie_details("Interstellar")
    print(details)

    # Repeat to test cache hit
    details_cached = get_movie_details("Interstellar")
    print("Repeated result:", details_cached)

    # 2. Movie search
    print("\n--- Movie Search ---")
    search_results = search_movie("Inter")
    print(search_results)

    # Repeat to test cache hit
    search_cached = search_movie("Inter")
    print("Repeated result:", search_cached)

    # 3. Semantic recommendations
    print("\n--- Semantic Recommendations ---")
    recommendations = recommend_semantic_movies("Interstellar")
    print(recommendations)

    # Repeat to test cache hit
    recommendations_cached = recommend_semantic_movies("Interstellar")
    print("Repeated result:", recommendations_cached)

    # Verify results are identical
    assert details == details_cached
    assert search_results == search_cached
    assert recommendations == recommendations_cached

    print("\nAll functional tests passed.")

# Main objective is to find movie with similar meanings from movie description/embedding is similar
