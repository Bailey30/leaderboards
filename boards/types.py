from typing import TypedDict, List
from dataclasses import dataclass


class MappedScores(TypedDict):
    username: str
    value: int


class Leaderboard(TypedDict):
    id: str
    name: str
    scores: List[MappedScores]


class LeaderboardInfo(TypedDict):
    id: str
    name: str


@dataclass
class Score:
    username: str
    value: int

    def mapping(self):
        return {self.username: self.value}


type Username = str
type ScoreValue = str
type ScoreTuple = tuple[Username, ScoreValue]
