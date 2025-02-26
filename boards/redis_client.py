from typing import Dict, List
import redis

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


def add_sorted_set_value(key, value: Dict[str, str]) -> None:
    added = redis_client.zadd(key, value)
    print("added: ", added)


def get_sorted_set(key) -> List:
    sorted_set = redis_client.zrevrange(key, 0, 10, withscores=True)
    return sorted_set


def add_hash(key, mappings) -> None:
    added = redis_client.hset(key + ":info", mapping=mappings)
    print("added: ", added)


def get_hash(key) -> Dict:
    return redis_client.hgetall(key + ":info")
