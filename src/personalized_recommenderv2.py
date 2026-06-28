from user_profile import get_user_summary
from semantic_recommender import recommend_semantic_movies
from collaborative_filter_v2 import recommend_cf_movies


def recommend_for_user(username):

    user_data = get_user_summary(username)

    liked_movies = user_data.get("liked_movies", [])

    movie_scores = {}

    for movie in liked_movies:

        print(f"\n{'='*50}")
        print(f"PROCESSING LIKED MOVIE : {movie}")
        print(f"{'='*50}")

        # SEMANTIC 

        semantic_results = recommend_semantic_movies(movie)

        for rec in semantic_results:

            title = rec["title"]

            if title not in movie_scores:

                movie_scores[title] = {
                    "title": title,
                    "rating": rec["rating"],
                    "year": rec["year"],
                    "semantic_score": rec["similarity_score"],
                    "cf_score": 0,
                    "recommendation_score": 1,
                    "source": ["semantic"]
                }

            else:

                movie_scores[title]["recommendation_score"] += 1

                movie_scores[title]["source"].append("semantic")

                movie_scores[title]["semantic_score"] = max(
                    movie_scores[title]["semantic_score"],
                    rec["similarity_score"]
                )

        # CF

        cf_results = recommend_cf_movies(movie)

        for rec in cf_results:

            title = rec["title"]

            if title not in movie_scores:

                movie_scores[title] = {
                    "title": title,
                    "rating": 0,
                    "year": "",
                    "semantic_score": 0,
                    "cf_score": rec["cf_score"],
                    "recommendation_score": 1,
                    "source": ["cf"]
                }

            else:

                movie_scores[title]["recommendation_score"] += 1

                movie_scores[title]["source"].append("cf")

                movie_scores[title]["cf_score"] = max(
                    movie_scores[title]["cf_score"],
                    rec["cf_score"]
                )


    final_recommendations = sorted(

        movie_scores.values(),

        key=lambda x: x["recommendation_score"],

        reverse=True

    )

    print("\n")
    print("=" * 60)
    print("FINAL RECOMMENDATIONS")
    print("=" * 60)

    for movie in final_recommendations[:10]:

        print(movie)

    return final_recommendations[:10]


if __name__ == "__main__":

    recommend_for_user("shiva")