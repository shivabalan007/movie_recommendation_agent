from src.database.cache import cache_get, cache_set, cache_delete

key = "test:movie:interstellar"
movie = {
    "title": "Interstellar",
    "year": 2014,
    "rating": 8.5,
}

# Clear any old test value
cache_delete(key)

# Cache miss
print("Before caching:", cache_get(key))

# Store a value with a 60-second TTL
print("Cache write successful:", cache_set(key, movie, ttl=60))

# Cache hit
print("After caching:", cache_get(key))

# Delete and verify
print("Deleted:", cache_delete(key))
print("After deletion:", cache_get(key))
