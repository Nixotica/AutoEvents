from abc import ABC

from src.api.structure.enums import SpotType


class MatchSpot(ABC):
    def __init__(
        self,
        spot_type: SpotType,
    ):
        self._spot_type = spot_type


class QualificationMatchSpot(MatchSpot):
    def __init__(
        self,
        round_position: int,
        rank: int,
    ):
        super().__init__(SpotType.QUALIFICATION)
        self._round_position = round_position
        self._rank = rank


class SeedMatchSpot(MatchSpot):
    def __init__(
        self,
        seed: int,
    ):
        super().__init__(SpotType.SEED)
        self._seed = seed


class CompetitionMatchSpot(MatchSpot):
    def __init__(
        self,
        rank: int,
    ):
        super().__init__(SpotType.COMPETITION)
        self._rank = rank
