from typing import Dict, List
import redis

from boards.utils import map_scores

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


def get_all_leaderboard():
    leaderboard_keys = redis_client.scan_iter("leaderboard:*:info")
    leaderboards = []

    for key in leaderboard_keys:
        board_info = redis_client.hgetall(key)
        scores = get_sorted_set(f"leaderboard:{board_info['id']}")

        data = {**board_info, "scores": map_scores(scores)}
        leaderboards.append(data)

    return leaderboards
