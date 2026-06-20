import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load data
movie_ratings = pd.read_csv(
    r"C:\Dev\projects\movie_recommemdation_agent\data\processed\movie_ratings.csv"
)

# User-movie matrix
user_movie_matrix = movie_ratings.pivot_table(
    index="user_id",
    columns="movie_title",
    values="ratings"
)

# row - user & columns - movie_title
user_movie_matrix_filled = user_movie_matrix.fillna(0)

# Movie similarity matrix
movie_similarity = cosine_similarity(
    user_movie_matrix_filled.T
)

# row - movie_title  & columns - user
# To view this we need to change to Data Frame
movie_similarity_df = pd.DataFrame(
    movie_similarity,
    index=user_movie_matrix.columns,
    columns=user_movie_matrix.columns
)

def recommend_movies(movie_name, num_recommendations=10):
    matches = []
    for movie in movie_similarity_df.columns:
        if movie_name.lower() in movie.lower():
            matches.append(movie)

    if len(matches) == 0:
        return ["Movie not found"]
    
    matched_movie = matches[0]

    similar_movies = movie_similarity_df[
        matched_movie
    ].sort_values(
        ascending=False
    )

    recommendations = similar_movies.iloc[
        1:num_recommendations + 1
    ]

    return recommendations.index.tolist()
