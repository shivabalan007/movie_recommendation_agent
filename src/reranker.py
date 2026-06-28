from personalized_recommenderv2 import recommend_for_user
from genre_service import get_movie_genres
from user_profile import get_user_summary


def genre_rerank(recommendations, username):

    user = get_user_summary(username)

    genre_profile = user.get("genre_profile", {})

    for movie in recommendations:

        genres = get_movie_genres(movie["title"])

        movie["genres"] = genres

        genre_match = 0

        for genre in genres:
            genre_match += genre_profile.get(genre,0)

        movie["genre_match"] = genre_match

    recommendations = sorted(
        recommendations,
        key=lambda movie: (
            movie["recommendation_score"],
            movie["genre_match"]
        ),
        reverse=True
    )

    return recommendations


if __name__ == "__main__":

    recommendations = recommend_for_user("shiva")

    final = genre_rerank(
        recommendations,
        "shiva"
    )

    print("\n========== FINAL RE-RANKED RECOMMENDATIONS ==========\n")

    for movie in final:
        print(movie)