from typing import List, TypedDict
from .types import MappedScores, ScoreTuple


def map_scores(scores: List[ScoreTuple]) -> List[MappedScores]:
    """
    Takes a list of Tuples that contain the username and score as returned from the Redis sorted set: ("username", 111111)
    Return a list of dictionarys with the username and score mapped to keys.
    """
    return [{"username": x, "value": int(y)} for (x, y) in scores]
