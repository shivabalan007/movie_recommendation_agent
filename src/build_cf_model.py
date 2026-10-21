import os
import joblib
import pandas as pd

# Load datasets

ratings = pd.read_csv(
    r"C:\Dev\projects\movie_recommendation_agent\data\raw\movie_lens_latest\ratings.csv"
)

movies = pd.read_csv(
    r"C:\Dev\projects\movie_recommendation_agent\data\raw\movie_lens_latest\movies.csv"
)

# Merge ratings with movie titles

movie_ratings = ratings.merge(
    movies,
    on="movieId"
)

# Movie-User Matrix

movie_user_matrix = movie_ratings.pivot_table(
    index="title",
    columns="userId",
    values="rating"
).fillna(0)

# Save artifacts

MODEL_DIR = r"C:\Dev\projects\movie_recommendation_agent\data\models"

os.makedirs(
    MODEL_DIR,
    exist_ok=True
)

joblib.dump(
    movie_user_matrix,
    os.path.join(
        MODEL_DIR,
        "movie_user_matrix.pkl"
    )
)

print("Movie User Matrix Saved Successfully!")
print(movie_user_matrix.shape)