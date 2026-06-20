import pandas as pd
import joblib

latest_movies = pd.read_csv(
    r"C:\Dev\projects\movie_recommemdation_agent\data\processed\latest_movies_final.csv"
)

similarity_matrix = joblib.load(
    r"C:\Dev\projects\movie_recommemdation_agent\data\embeddings\similarity_matrix.pkl"
)

#Movie title -> index mapping
movie_indices = pd.Series(
    latest_movies.index,
    index=latest_movies["title"]
).drop_duplicates()

def recommend_semantic_movies(movie_name, num_recommendation=10):
    matches = []
    for title in movie_indices.index:
        if movie_name.lower() in title.lower():
            matches.append(title)
    if len(matches) == 0:
        return ["Movie not found"]

    matched_movie = matches[0]

    movie_index = movie_indices[matched_movie]

    similarity_scores = list(
        enumerate(
            similarity_matrix[movie_index]
        )
    )

    similarity_scores = sorted(
        similarity_scores,
        key=lambda x:x[1],
        reverse=True
    )

    top_movies = similarity_scores[
        1:num_recommendation + 1
    ]

    recommendations = []

    for movie in top_movies:
        row = latest_movies.iloc[movie[0]]
        recommendations.append({
    "title": row["title"],
    "rating": round(float(row["vote_average"]), 1),
    "year": str(row["release_date"])[:4]
})


    return recommendations

def search_movie(query):
    matches = []

    for title in latest_movies["title"]:
        if query.lower() in title.lower():
            matches.append(title)

    return matches[:10]


def get_movie_details(movie_name):
    """
    Returns movie details.
    """

    movie = latest_movies[
        latest_movies["title"].str.lower() == movie_name.lower()
    ]

    if movie.empty:
        return None

    movie = movie.iloc[0]

    return {
        "title": movie["title"],
        "overview": movie["overview"],
        "rating": round(float(movie["vote_average"]), 1),
        "release_year": str(movie["release_date"])[:4]
    }
