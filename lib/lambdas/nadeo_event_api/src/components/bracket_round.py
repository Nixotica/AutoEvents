from abc import abstractmethod
from datetime import datetime
from typing import List
from api.structure.round.match import Match
from api.structure.enums import LeaderboardType, SpotType
from api.structure.round.qualifier import Qualifier
from api.structure.round.round import Round, RoundConfig


class BracketRound(Round):
    def __init__(
        self,
        name: str,
        start_date: datetime,
        end_date: datetime,
        num_matches: int,
        players_per_match: int,
        spot_type: SpotType,
        round_config: RoundConfig,
        qualifier: Qualifier = None,
    ):
        self._num_matches = num_matches
        self._players_per_match = players_per_match
        self._spot_type = spot_type

        super().__init__(
            name,
            start_date,
            end_date,
            self.get_matches(),
            LeaderboardType.BRACKET,
            round_config,
            qualifier,
        )

    @abstractmethod
    def get_matches(self) -> List[Match]:
        """
        Gets matches for a bracket round based on its spot type and number of matches.
        """
