from typing import List
from nadeo_event_api.src.api.structure.round.round import Round


class SpotStructure:
    def __init__(
        self,
        rounds: List[Round],
        version: int = 0,
        match_generator_type: str = "spot_filler",
    ):
        self._rounds = rounds
        self._version = version
        self._match_generator_type = match_generator_type

    def as_jsonable_dict(self) -> dict:
        spot_structure = {}
        spot_structure["version"] = self._version
        spot_structure["rounds"] = [
            {
                "name": round._name,
                "matchGeneratorData": {
                    "matches": [match.as_jsonable_dict() for match in round._matches]
                },
                "matchGeneratorType": self._match_generator_type,
            }
            for round in self._rounds
        ]
        return spot_structure
