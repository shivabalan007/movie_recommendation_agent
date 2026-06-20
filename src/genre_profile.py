import pandas as pd
import re

from user_profile import get_user_summary
from user_profile import load_profiles
from user_profile import save_profiles

movies = pd.read_csv(
    r"C:\Dev\projects\movie_recommemdation_agent\data\raw\movie_lens_latest\movies.csv"
)

IGNORE_GENRES = {
    "IMAX",
    #"(no genres listed)"
}


def clean_title(title):

    return re.sub(
        r"\(\d{4}\)",
        "",
        title
    ).strip().lower()


movie_genres = {}

for _, row in movies.iterrows():

    title = clean_title(
        row["title"]
    )

    movie_genres[title] = row["genres"]


def build_genre_profile(username):

    data = get_user_summary(username)

    liked_movies = data.get(
        "liked_movies",
        []
    )

    genre_counts = {}

    for movie in liked_movies:

        genres = movie_genres.get(
            movie.lower(),
            ""
        )

        genres = genres.split("|")

        for genre in genres:

            if genre in IGNORE_GENRES:
                continue

            genre_counts[genre] = (
                genre_counts.get(
                    genre,
                    0
                ) + 1
            )

    return genre_counts

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

    top_genres = get_top_genres(
        username,
        top_n=1
    )

    if top_genres:
        return top_genres[0][0]

    return None

if __name__ == "__main__":

    profile = build_genre_profile(
        "shiva"
    )
    
    update_genre_profile(
        "shiva",
        profile
    )