from typing import Dict, List

import redis.asyncio as redis

# import aioredis
from dataclasses import asdict, dataclass

from boards.utils import map_scores

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
# redis_client = aioredis.from_url(
#     "redis://localhost", port=6376, db=0, decode_responses=True
# )


@dataclass
class LeaderboardInfo:
    id: str
    name: str


@dataclass
class Score:
    username: str
    value: int

    def mapping(self):
        return {self.username: self.value}


async def save_score(board_id, score: Score) -> None:
    leaderboard_key = f"leaderboard:{board_id}"
    print("score: ", asdict(score))
    added = await redis_client.zadd(leaderboard_key, score.mapping())
    print("added: ", added)


async def get_scores_for_leaderboard(board_id) -> List:
    leaderboard_key = f"leaderboard:{board_id}"
    print("leaderboard key:", leaderboard_key)
    sorted_set = await redis_client.zrevrange(leaderboard_key, 0, 10, withscores=True)
    return sorted_set


async def save_leaderboard_info(board_id, mappings) -> None:
    """
    Saves information about a leaderboard to a Redis Hash.
    Info includes id and name.
    """

    leaderboard_key = f"leaderboard:{board_id}:info"
    added = await redis_client.hset(leaderboard_key, mapping=mappings)

    print("added: ", added)


async def get_leaderboard(board_id) -> Dict:
    leaderboard_key = f"leaderboard:{board_id}:info"
    board = await redis_client.hgetall(leaderboard_key)
    print("board:", board)
    return board


async def get_all_leaderboards():
    leaderboard_keys = redis_client.scan_iter("leaderboard:*:info")
    leaderboards = []

    async for key in leaderboard_keys:
        board_info = await redis_client.hgetall(key)
        print("board info:", board_info)
        scores = await get_scores_for_leaderboard(board_info["id"])

        data = {**board_info, "scores": map_scores(scores)}
        leaderboards.append(data)

    return leaderboards
