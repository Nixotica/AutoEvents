from typing import List
from src.api.structure.round.round import Round


class SpotStructure:
    def __init__(
        self,
        rounds: List[Round],
    ):
        self._rounds = rounds

    def as_jsonable_dict(self):
        pass
