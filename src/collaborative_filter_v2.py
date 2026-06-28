import pandas as pd
import re
from sklearn.metrics.pairwise import cosine_similarity

# Load Data

ratings = pd.read_csv(
    r"C:\Dev\projects\movie_recommemdation_agent\data\raw\movie_lens_latest\ratings.csv"
)

movies = pd.read_csv(
    r"C:\Dev\projects\movie_recommemdation_agent\data\raw\movie_lens_latest\movies.csv"
)

# Merge Ratings + Movies

movie_ratings = ratings.merge(
    movies,
    on="movieId"
)

# Create Movie-User matrix
# Row -> Movie & Columns -> User

movie_user_matrix = movie_ratings.pivot_table(
    index="title",
    columns="userId",
    values="rating"
).fillna(0)

# Cosine Similarity

movie_similarity = cosine_similarity(
    movie_user_matrix
)

# This measure how similar every movie is to every other movie
similarity_df = pd.DataFrame(
    movie_similarity,
    index=movie_user_matrix.index,
    columns=movie_user_matrix.index
)

def clean_title(title):
    return re.sub(r"\(\d{4}\)","",title).strip()

def find_movie_title(movie_name):
    movie_name = movie_name.lower().strip()

    for title in movie_user_matrix.index:
        clean_text = re.sub(
            r"\(\d{4}\)",
            "",
            title
        ).strip().lower()

        if clean_text == movie_name:
            return title
    return None

def recommend_cf_movies(movie_name, top_n=10):

    movie_title = find_movie_title(movie_name)

    if movie_title is None:
        print(f"Movie '{movie_name}' not found.")
        return []

    recommendations = (
        similarity_df[movie_title]
        .sort_values(ascending=False)
        .iloc[1:top_n + 1]
    )

    results = []

    for title, score in recommendations.items():

        results.append({
            "title": clean_title(title),
            "cf_score": round(float(score),3)
        })

    return results

def search_movie(movie_name):

    matches = [
        title
        for title in movie_user_matrix.index
        if movie_name.lower() in title.lower()
    ]

    return matches[:20]

if __name__ == "__main__":

    movie = "Interstellar"

    recommendations = recommend_cf_movies(movie)

    print("\nCollaborative Filtering Recommendations:\n")

    for idx, rec in enumerate(recommendations, start=1):
        print(f"{idx}. {rec}")

# Main objective is People who liked x also like y - People who liked similar movies also liked this.