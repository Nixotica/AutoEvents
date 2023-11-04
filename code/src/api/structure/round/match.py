from typing import List

from src.api.structure.round.match_spot import MatchSpot


class Match:
    def __init__(
        self,
        spots: List[MatchSpot],
    ):
        self._spots = spots
