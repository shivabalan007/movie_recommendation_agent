from collaborative_filter import recommend_movies
from semantic_recommender import recommend_semantic_movies

def hybrid_recommend(movie_name):

    try:
        collaborative = recommend_movies(movie_name)
    except:
        collaborative = []

    try:
        semantic = recommend_semantic_movies(movie_name)
    except:
        semantic = []

    return {
        "collaborative": collaborative,
        "semantic": semantic
    }