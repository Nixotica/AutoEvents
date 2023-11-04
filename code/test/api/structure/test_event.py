from datetime import datetime
import unittest
import json
from src.api.structure.maps import Map, MapPool
from src.api.structure.enums import LeaderboardType
from src.api.structure.round.match_spot import SeedMatchSpot
from src.api.structure.round.match import Match
from src.api.structure.round.round import Round, RoundConfig

from src.api.structure.event import Event


class TestEvent(unittest.TestCase):
    def test_basic_event_as_jsonable_dict(self):
        with open("resources/basic_event.json") as f:
            expected = json.load(f)
        actual = Event(
            name="my_event",
            club_id=123,
            description="my_description",
            registration_start_date=datetime(2023, 11, 3, 20, 45),
            registration_end_date=datetime(2023, 11, 3, 20, 55),
            rounds=[
                Round(
                    name="round_1",
                    start_date=datetime(2023, 11, 3, 20, 55),
                    end_date=datetime(2023, 11, 3, 21, 5),
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
                    ),
                ),
            ],
        )
