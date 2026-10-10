from src.database.redis_connection import redis_client

print("Redis ping:", redis_client.ping())