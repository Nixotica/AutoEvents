from abc import abstractmethod
from datetime import datetime
from typing import List
from api.structure.round.qualifier import Qualifier
from api.structure.round.round import Round
from components.enums import BracketType
from api.structure.event import Event


class BracketEvent(Event):
    def __init__(
        self,
        name: str,
        club_id: int,
        bracket_type: BracketType,
        description: str = None,
        registration_start_date: datetime = None,
        registration_end_date: datetime = None,
        max_players: int = None,
        qualifier: Qualifier = None,
    ):
        self._bracket_type = bracket_type
        self._max_players = max_players
        self._qualifier = qualifier

        super().__init__(
            name,
            club_id,
            self.get_rounds(),
            description,
            registration_start_date,
            registration_end_date,
        )

    @abstractmethod
    def get_rounds(self) -> List[Round]:
        """
        Generates the rounds for a bracket event.
        """
        pass
