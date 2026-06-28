import pandas as pd

from user_profile import get_user_summary
from user_profile import load_profiles
from user_profile import save_profiles
from genre_service import get_movie_genres


def build_genre_profile(username):

    data = get_user_summary(username)

    liked_movies = data.get("liked_movies",[])

    genre_counts = {}

    for movie in liked_movies:
        genres = get_movie_genres(movie)

        # print(f"Movie: {movie}")   ''' Testing '''
        # print(f"Genres: {genres}")

        for genre in genres:
            genre_counts[genre] = (genre_counts.get(genre, 0)+1)
            

    return genre_counts

def update_genre_profile(username, genre_profile):
    profiles = load_profiles()

    profiles[username]["genre_profile"] = genre_profile

    save_profiles(profiles)

def get_top_genres(username, top_n=3):

    data = get_user_summary(username)

    genre_profile = data.get("genre_profile",{})

    return sorted(
        genre_profile.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

def get_favorite_genre(username):

    top_genres = get_top_genres(
        username,
        top_n=1
    )

    if top_genres:
        return top_genres[0][0]

    return None

def update_genre_profile(username, genre_profile):
    profiles = load_profiles()

    profiles[username]["genre_profile"] = genre_profile

    save_profiles(profiles)

def get_top_genres(username, top_n=3):

    data = get_user_summary(username)

    genre_profile = data.get(
        "genre_profile",
        {}
    )

    return sorted(
        genre_profile.items(),
        key=lambda x: x[1],
        reverse=True
    )[:top_n]

def get_favorite_genre(username):

    top_genres = get_top_genres(username,top_n=1)

    if top_genres:
        return top_genres[0][0]

    return None

def refresh_genre_profile(username):

    genre_profile = build_genre_profile(username)

    update_genre_profile(
        username,
        genre_profile
    )

    return genre_profile

if __name__ == "__main__":

    genre_profile = build_genre_profile('shiva')
    print(genre_profile)
    
    # update_genre_profile("shiva", genre_profile)

    print(get_top_genres("shiva"))
    print(get_favorite_genre("shiva"))



# Main objective is to build genre_profile for respective user and computes user preference.