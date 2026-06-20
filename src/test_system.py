from collaborative_filter import recommend_movies
from semantic_recommender import recommend_semantic_movies

# print("\nCollaborative Filtering:\n")

# print(recommend_movies("Star Wars"))

# print("\nSemantic Recommender:\n")

# print(recommend_semantic_movies("Interstellar"))


from semantic_recommender import (
    get_movie_details,
    recommend_semantic_movies
)

movie_name = input("Enter movie: ")
details = get_movie_details(movie_name)

if details is None:
    print("Movie not found")
else:
    print("\n Movie Details")
    print("-" * 12)

    print(f"Title: {details['title']}")
    print(f"Year: {details['release_year']}")
    print(f"Rating: {details['rating']}")

    print("\nRecommendations")
    print("-" * 15)

    recommendations = recommend_semantic_movies(movie_name, 15)

    for i, movie in enumerate(recommendations, start=1):
        print(
            f"{i}. {movie['title']}"
            f"({movie['year']})"
            f"Rating: {movie['rating']}"
        )