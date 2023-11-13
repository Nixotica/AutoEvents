from datetime import datetime, timedelta
from src.environment import UBI_AUTH
from test.util import are_json_structures_equal
from src.constants import CLUB_AUTO_EVENTS_STAGING
import pytest
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
    def test_basic_event_as_jsonable_dict(self):
        with open("nadeo_event_api/test/api/structure/resources/basic_event.json") as f:
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

        self.assertTrue(are_json_structures_equal(expected, actual))

    @pytest.mark.integration
    def test_post_and_delete_event(self):
        now = datetime.utcnow()
        event = Event(
            name="my_event",
            club_id=CLUB_AUTO_EVENTS_STAGING,
            rounds=[
                Round(
                    name="round_1",
                    start_date=now + timedelta(minutes=50),
                    end_date=now + timedelta(minutes=80),
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
                            Map("_jTSBKAuePtwJ2tUz8UZx25rYzl"),
                        ],
                        script=ScriptType.CUP,
                        max_players=32,
                    ),
                    qualifier=Qualifier(
                        name="qualifier_1",
                        start_date=now + timedelta(minutes=10),
                        end_date=now + timedelta(minutes=40),
                        leaderboard_type=LeaderboardType.SUM,
                        config=QualifierConfig(
                            map_pool=[Map("_jTSBKAuePtwJ2tUz8UZx25rYzl")],
                            script=ScriptType.TIME_ATTACK,
                            max_players=64,
                        ),
                    ),
                ),
            ],
        )
        auth = os.getenv(UBI_AUTH)
        event.post(auth)
        self.assertIsNotNone(event._registered_id)
        event.delete(auth)
        self.assertIsNone(event._registered_id)
