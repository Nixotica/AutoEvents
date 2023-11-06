from datetime import datetime
import os
import unittest
import json
from src.api.structure.round.qualifier import Qualifier, QualifierConfig
from src.api.structure.maps import Map
from src.api.structure.enums import LeaderboardType, ScriptType
from src.api.structure.round.match_spot import SeedMatchSpot
from src.api.structure.round.match import Match
from src.api.structure.round.round import Round, RoundConfig

from src.api.structure.event import Event


class TestEvent(unittest.TestCase):
    def deep_sort(self, obj):
        """
        Recursively sort list or dict nested lists.
        """

        if isinstance(obj, dict):
            # Sort the dictionary by key, then sort the values recursively
            return {k: self.deep_sort(obj[k]) for k in sorted(obj)}
        elif isinstance(obj, list):
            # Attempt to sort the list. If this fails (e.g., if it contains dictionaries),
            # sort each item in the list recursively and turn them into tuples if they are dictionaries
            try:
                return sorted(self.deep_sort(x) for x in obj)
            except TypeError:
                # The list contains non-orderable items (like dictionaries), sort them as tuples
                return sorted(
                    (k, self.deep_sort(v)) if isinstance(v, dict) else self.deep_sort(v)
                    for k, v in (x.items() for x in obj)
                )
        else:
            # If obj is not a list or dict, return it as is
            return obj

    def are_json_structures_equal(self, json1: dict, json2: dict):
        """
        Check if the given JSON structures are equal, after sorting them recursively.
        """
        sorted_json1 = self.deep_sort(json1)
        sorted_json2 = self.deep_sort(json2)

        with open("expected.json", "w") as f:
            json.dump(sorted_json1, f)
        with open("actual.json", "w") as f:
            json.dump(sorted_json2, f)

        return sorted_json1 == sorted_json2

    def test_basic_event_as_jsonable_dict(self):
        with open("code/test/api/structure/resources/basic_event.json") as f:
            expected: dict = json.load(f)
        actual = Event(
            name="my_event",
            club_id=123,
            description="my_description",
            registration_start_date=datetime(2023, 11, 3, 20, 45),
            registration_end_date=datetime(2023, 11, 3, 20, 55),
            rounds=[
                Round(
                    name="round_1",
                    start_date=datetime(2023, 11, 3, 21, 5),
                    end_date=datetime(2023, 11, 3, 21, 15),
                    matches=[
                        Match(
                            spots=[
                                SeedMatchSpot(
                                    seed=1,
                                ),
                                SeedMatchSpot(
                                    seed=2,
                                ),
                            ],
                        ),
                    ],
                    leaderboard_type=LeaderboardType.BRACKET,
                    config=RoundConfig(
                        map_pool=[
                            Map("round_map"),
                        ],
                        script=ScriptType.CUP,
                        max_players=32,
                    ),
                    qualifier=Qualifier(
                        name="qualifier_1",
                        start_date=datetime(2023, 11, 3, 20, 55),
                        end_date=datetime(2023, 11, 3, 21, 5),
                        leaderboard_type=LeaderboardType.SUM,
                        config=QualifierConfig(
                            map_pool=[Map("quali_map")],
                            script=ScriptType.TIME_ATTACK,
                            max_players=64,
                        ),
                    ),
                ),
            ],
        )._as_jsonable_dict()

        self.assertTrue(self.are_json_structures_equal(expected, actual))
