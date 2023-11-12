from datetime import datetime, timedelta
from math import ceil, log2
from typing import List
from src.api.structure.maps import Map
from src.api.structure.enums import ScriptType, SpotType
from src.api.structure.round.qualifier import Qualifier
from src.components.single_elim.single_elim_bracket_round import SingleElimBracketRound
from src.api.structure.round.round import Round, RoundConfig
from src.components.enums import BracketType
from src.components.bracket_event import BracketEvent


class SingleElimBracketEvent(BracketEvent):
    def __init__(
        self,
        name: str,
        club_id: int,
        max_players: int,  # For now, this is mandatory since we can't know the number of rounds unless there's a system to check the number of players who played the qualifier or registered
        players_per_match: int,
        start_date: datetime,
        time_per_round_minutes: int,
        map_pool: List[Map],
        script: ScriptType,
        description: str = None,
        registration_start_date: datetime = None,
        registration_end_date: datetime = None,
        qualifier: Qualifier = None,
    ):
        self._players_per_match = players_per_match
        self._start_date = start_date
        self._time_per_round_minutes = time_per_round_minutes
        self._map_pool = map_pool
        self._script = script

        super().__init__(
            name,
            club_id,
            BracketType.SINGLE_ELIM,
            qualifier,
            description,
            registration_start_date,
            registration_end_date,
            max_players,
        )

    def get_rounds(self) -> List[Round]:
        """
        Generates the rounds for a single elim bracket event.
        """

        rounds = []

        # Get the max players, then make N rounds where 2^N >= max_players.
        num_rounds = ceil(log2(self._max_players))

        round_start_offset_min = (
            0
            if not self._qualifier
            else (
                self._qualifier._end_date - self._qualifier._start_date
            ).total_seconds()
            // 60
        )
        for i in range(num_rounds):
            round_start = self._start_date + timedelta(minutes=round_start_offset_min)
            rounds.append(
                SingleElimBracketRound(
                    self._name,
                    round_start,
                    round_start + timedelta(minutes=self._time_per_round_minutes),
                    2 ** (num_rounds - i - 1),
                    self._players_per_match,
                    SpotType.QUALIFICATION,
                    self.get_round_config(),
                    self._qualifier,
                )
            )
            round_start_offset_min += self._time_per_round_minutes

        return rounds

    def get_round_config(self) -> RoundConfig:
        """
        Gets a round config for single elim bracket.
        """
        # TODO allow override of more settings here
        return RoundConfig(
            self._map_pool,
            self._script,
            self._max_players,
        )
