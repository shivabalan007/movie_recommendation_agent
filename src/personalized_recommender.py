from user_profile import get_user_summary
from semantic_recommender import recommend_semantic_movies


def recommend_for_user(username):
    data = get_user_summary(username)

    liked_movies = data.get("liked_movies",[])

    all_recommendations = []

    for movie in liked_movies:
        recommendations = recommend_semantic_movies(movie)

        all_recommendations.extend(recommendations)
    
    movie_scores = {}

    liked_movies_set = set(liked_movies)

    for movie in all_recommendations:
        title = movie["title"]
        
        if title in liked_movies_set:
            continue
        
        if title not in movie_scores:
            movie_scores[title] = {"movie": movie, "score":1}
        else:
            movie_scores[title]["score"] += 1
    
    ranked_movies = sorted(
        movie_scores.values(),
        key=lambda x:x["score"],
        reverse=True
    )

    final_recommendation = []

    for item in ranked_movies:
        movie = item["movie"]
        movie["recommendation_score"] = item["score"]
        final_recommendation.append(movie)

    return final_recommendation[:10]

if __name__ == "__main__":
    recommendations = recommend_for_user("shiva")

    print(recommendations)