from datetime import datetime
from typing import List
from src.api.structure.round.match import Match
from src.api.structure.round.round import RoundConfig
from src.api.structure.round.qualifier import Qualifier
from src.api.structure.enums import SpotType
from src.components.bracket_round import BracketRound


class SingleElimBracketRound(BracketRound):
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
        super().__init__(
            name,
            start_date,
            end_date,
            num_matches,
            players_per_match,
            spot_type,
            round_config,
            qualifier,
        )

    def get_matches(self) -> List[Match]:
        """
        Gets the matches for a single elim bracket round based on its spot type and number of matches.
        """
