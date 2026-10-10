import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from src.utils import clean_title

# Load Saved Matrix
movie_user_matrix = joblib.load(
    r"C:\Dev\projects\movie_recommemdation_agent\data\models\movie_user_matrix.pkl"
)

def find_movie_title(movie_name):

    movie_name = movie_name.lower().strip()

    for title in movie_user_matrix.index:

        clean = clean_title(title).lower()

        if clean == movie_name:
            return title

    return None


# Recommendation

def recommend_cf_movies(movie_name, top_n=10):

    movie_title = find_movie_title(movie_name)

    if movie_title is None:
        return []

    # Compute similarity ONLY for requested movie against all other movie
    similarity_scores = cosine_similarity(
        movie_user_matrix.loc[[movie_title]],
        movie_user_matrix
    )[0]

    similarity_series = pd.Series(
        similarity_scores,
        index=movie_user_matrix.index
    )

    recommendations = similarity_series.sort_values(
        ascending=False
    ).iloc[1:top_n + 1]

    results = []

    for title, score in recommendations.items():

        results.append(
            {
                "title": clean_title(title),
                "cf_score": round(float(score), 3)
            }
        )

    return results


# Search

def search_movie(movie_name):

    movie_name = movie_name.lower()

    matches = []

    for title in movie_user_matrix.index:

        if movie_name in title.lower():

            matches.append(clean_title(title))

    return matches[:20]


if __name__ == "__main__":

    recommendations = recommend_cf_movies(
        "Alien"
    )

    for movie in recommendations:
        print(movie)

# Main objective is People who liked x also like y - People who liked similar movies also liked this.