from typing import Dict


def map_scores(scores) -> Dict:
    return [{"username": x, "value": int(y)} for (x, y) in scores]
