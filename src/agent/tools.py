from langchain_core.tools import tool
from src.semantic_recommender import(search_movie, get_movie_details, recommend_semantic_movies)
from src.collaborative_filter_v2 import(recommend_cf_movies)
from src.personalized_recommenderv2 import(recommend_for_user)
from src.reranker import genre_rerank

@tool
def search_movie_tool(query: str):
    """ Search movies by partial or full movie title Return up to 10 matching movie title"""
    return search_movie(query) # Name, Description and Parameter

@tool
def movie_details_tool(movie_name: str):
    """ Get detailed information about movie. return title, overview, ratings and release year"""
    return get_movie_details(movie_name)

@tool
def semantic_recommendation_tool(movie_name: str):
    """ Recommend movies similar to the given movie using semantic similarity. """
    return recommend_semantic_movies(movie_name)


@tool
def collaborative_recommendation_tool(movie_name: str):
    """ Recommend movies using collaborative filtering. """
    return recommend_cf_movies(movie_name)


@tool
def personalized_recommendation_tool(username: str):
    """ Recommend personalized movies for a user based on liked movies and recommendation frequency. """
    return recommend_for_user(username)


@tool
def genre_rerank_tool(username: str):
    """ Re-rank personalized recommendations according to the user's favourite genres. """
    recommendations = recommend_for_user(username)
    return genre_rerank(recommendations, username)


if __name__ == "__main__":
    print(search_movie_tool.name)
    print(search_movie_tool.description)

    print("--------------------------------")

    print(movie_details_tool.name)
    print(movie_details_tool.description)

    print("--------------------------------")

    print(semantic_recommendation_tool.name)
    print(semantic_recommendation_tool.description)

    print("--------------------------------")

    print(collaborative_recommendation_tool.name)
    print(collaborative_recommendation_tool.description)

    print("--------------------------------")

    print(personalized_recommendation_tool.name)
    print(personalized_recommendation_tool.description)