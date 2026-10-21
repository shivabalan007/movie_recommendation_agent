from src.database.cache import cache_get, cache_delete
from src.semantic_recommender import get_movie_details

movie_name = "Interstellar"
key = "movie_agent:details:"  # We'll inspect the actual key below.

# Call once to populate the cache if needed
first = get_movie_details(movie_name)

# Find the actual cached value by using the same key-generation logic
import hashlib
import json

params = {"movie_name": movie_name.strip().casefold()}
serialized = json.dumps(params, sort_keys=True, ensure_ascii=False)
digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
key = f"movie_agent:details:{digest}"

cached = cache_get(key)

print("First result:", first)
print("Redis cached value:", cached)
print("Cache exists:", cached is not None)

assert first == cached
print("Cache verification passed.")




# from src.database.cache import cache_get, cache_set, cache_delete

# key = "test:movie:interstellar"
# movie = {
#     "title": "Interstellar",
#     "year": 2014,
#     "rating": 8.5,
# }

# # Clear any old test value
# cache_delete(key)

# # Cache miss
# print("Before caching:", cache_get(key))

# # Store a value with a 60-second TTL
# print("Cache write successful:", cache_set(key, movie, ttl=60))

# # Cache hit
# print("After caching:", cache_get(key))

# # Delete and verify
# print("Deleted:", cache_delete(key))
# print("After deletion:", cache_get(key))

