from typing import Dict, List, TypedDict

import redis.asyncio as redis

from dataclasses import asdict, dataclass

from boards.utils import map_scores

from .types import Leaderboard, Score, ScoreTuple, LeaderboardInfo

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)


async def save_score(board_id, score: Score) -> None:
    leaderboard_key = f"leaderboard:{board_id}"
    print("score: ", asdict(score))
    added = await redis_client.zadd(leaderboard_key, score.mapping())
    print("added: ", added)


async def get_scores_for_leaderboard(board_id) -> List[ScoreTuple]:
    leaderboard_key = f"leaderboard:{board_id}"
    print("leaderboard key:", leaderboard_key)
    sorted_set = await redis_client.zrevrange(leaderboard_key, 0, 10, withscores=True)
    return sorted_set


async def aave_leaderboard_info(board_id, board_info: LeaderboardInfo) -> None:
    """
    Saves information about a leaderboard to a Redis Hash.
    Info includes id and name.
    """

    leaderboard_key = f"leaderboard:{board_id}:info"
    added = await redis_client.hset(leaderboard_key, mapping=board_info)

    print("added: ", added)


async def get_leaderboard(board_id) -> LeaderboardInfo:
    leaderboard_key = f"leaderboard:{board_id}:info"
    board = await redis_client.hgetall(leaderboard_key)
    print("board:", board)
    return board


async def get_all_leaderboards() -> Leaderboard:
    leaderboard_keys = redis_client.scan_iter("leaderboard:*:info")
    leaderboards = []

    async for key in leaderboard_keys:
        board_info = await redis_client.hgetall(key)
        print("board info:", board_info)
        scores = await get_scores_for_leaderboard(board_info["id"])

        data = {**board_info, "scores": map_scores(scores)}
        leaderboards.append(data)

    return leaderboards
