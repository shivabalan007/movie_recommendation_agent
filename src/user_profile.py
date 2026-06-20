import json 

profile_path = r"C:\Dev\projects\movie_recommemdation_agent\data\users\user_profiles.json"

def load_profiles():
    with open(profile_path,"r") as file:
        return json.load(file)
    
def save_profiles(data):
    with open(profile_path,"w") as file:
        json.dump(data,file,indent=4)

def add_to_history(username, movie):
    profiles = load_profiles()

    profiles[username]["watch_history"].append(
        movie
    )

    save_profiles(profiles)

def add_liked_movie(username, movie):
    profiles = load_profiles()

    profiles[username]["liked_movies"].append(
        movie
    )

    save_profiles(profiles)

def add_disliked_movie(username, movie):
    profiles = load_profiles()

    profiles[username]["disliked_movies"].append(
        movie
    )

    save_profiles(profiles)

def get_user_summary(username):
    profiles = load_profiles()

    return profiles[username]

#print(get_user_summary("shiva"))

# add_to_history("shiva","Interstellar")
# add_liked_movie("shiva","Interstellar")
# add_disliked_movie("shiva","Titanic")
