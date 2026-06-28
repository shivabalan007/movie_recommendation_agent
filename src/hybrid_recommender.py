from pprint import pprint
from semantic_recommender import recommend_semantic_movies
from collaborative_filter_v2 import recommend_cf_movies
from utils import clean_title


def recommend_hybrid(movie_name):
    semantic_results = recommend_semantic_movies(movie_name)

    cf_results = recommend_cf_movies(movie_name)
    #test
    semantic_titles = {
        movie["title"]
        for movie in semantic_results
    }

    cf_titles = {
        movie["title"]
        for movie in cf_results
    }

    print("\nOverlap Movie")
    print(semantic_titles & cf_titles)



    #----------------------------------
    movie_scores = {}
    
    # Semantic score
    for movie in semantic_results:
        title = movie["title"]

        movie_scores[title] = {
            "semantic_score": movie["similarity_score"],
            "cf_score": 0,
            "source": ["semantic"]
        }

    # CF score = 1
    for movie in cf_results:
        title = movie["title"]
        score = movie["cf_score"]

        if title in movie_scores:
            movie_scores[title]["cf_score"] = score
            movie[title]["source"].append("cf")
        else:
            movie_scores[title] = {
                "semantic_score": 0,
                "cf_score": score,
                "source": ["cf"]
            }

    return movie_scores

if __name__ == "__main__":

    results = recommend_hybrid("Interstellar")
    # results = recommend_hybrid("Alien")

    for movie, data in results.items():
        print(movie, data)

