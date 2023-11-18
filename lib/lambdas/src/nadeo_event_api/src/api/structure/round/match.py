from typing import List

from src.api.structure.round.match_spot import MatchSpot


class Match:
    def __init__(
        self,
        spots: List[MatchSpot],
        settings: List = [],
    ):
        self._spots = spots
        self._settings = settings

    def as_jsonable_dict(self) -> dict:
        match = {}
        match["spots"] = [spot.as_jsonable_dict() for spot in self._spots]
        match["settings"] = self._settings
        return match
