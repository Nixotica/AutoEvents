from datetime import datetime, timedelta
import os
from typing import List
from lib.lambdas.src.nadeo_event_api.src.api.club.campaign import Campaign
from lib.lambdas.src.nadeo_event_api.src.api.structure.enums import (
    LeaderboardType,
    ScriptType,
)
from lib.lambdas.src.nadeo_event_api.src.api.structure.event import Event
from lib.lambdas.src.nadeo_event_api.src.api.structure.maps import Map
from lib.lambdas.src.nadeo_event_api.src.api.structure.round.match import Match
from lib.lambdas.src.nadeo_event_api.src.api.structure.round.match_spot import (
    MatchParticipantMatchSpot,
    SeedMatchSpot,
)
from lib.lambdas.src.nadeo_event_api.src.api.structure.round.qualifier import (
    Qualifier,
    QualifierConfig,
)
from lib.lambdas.src.nadeo_event_api.src.api.structure.round.round import (
    Round,
    RoundConfig,
)
from lib.lambdas.src.nadeo_event_api.src.api.structure.settings import (
    PluginSettings,
    ScriptSettings,
)
from lib.lambdas.src.nadeo_event_api.src.environment import (
    CAMPAIGN_ID,
    CLUB_ID,
    EVENT_NAME,
    UBI_AUTH,
)


def get_event_start() -> datetime:
    """
    Returns datetime object set to upcoming saturday at 7:00pm UTC
    :return: datetime object
    """
    today = datetime.utcnow()
    days_until_saturday = (5 - today.weekday() + 7) % 7
    days_until_saturday = days_until_saturday if days_until_saturday > 0 else 7
    next_saturday = today + timedelta(days=days_until_saturday)
    return next_saturday.replace(hour=19, minute=0, second=0, microsecond=0)


def get_round_config(num_winners: int, map_pool: List[Map]) -> RoundConfig:
    return RoundConfig(
        map_pool=map_pool,
        script=ScriptType.CUP,
        max_players=4,
        plugin_settings=PluginSettings(
            auto_start_delay=300,
            pick_ban_start_auto=True,
            pick_ban_order="b:0,p:1,p:2,p:3,p:0",
        ),
        script_settings=ScriptSettings(
            points_limit=120,
            number_of_winners=num_winners,
            rounds_per_map=4,
            warmup_duration=15,
        ),
    )


def get_qualifier(
    start_date: datetime, end_date: datetime, map_pool: List[Map]
) -> Qualifier:
    return Qualifier(
        name="Qualifier",
        start_date=start_date,
        end_date=end_date,
        leaderboard_type=LeaderboardType.SUM,
        config=QualifierConfig(
            map_pool=map_pool,
            script=ScriptType.TIME_ATTACK,
        ),
    )


def get_round_1(
    start_date: datetime,
    end_date: datetime,
    round_config: RoundConfig,
    qualifier: Qualifier,
) -> Round:
    return Round(
        name="Quarter Finals",
        start_date=start_date,
        end_date=end_date,
        matches=[
            Match(
                [
                    SeedMatchSpot(1),
                    SeedMatchSpot(8),
                    SeedMatchSpot(9),
                    SeedMatchSpot(16),
                ]
            ),
            Match(
                [
                    SeedMatchSpot(2),
                    SeedMatchSpot(7),
                    SeedMatchSpot(10),
                    SeedMatchSpot(15),
                ]
            ),
            Match(
                [
                    SeedMatchSpot(3),
                    SeedMatchSpot(6),
                    SeedMatchSpot(11),
                    SeedMatchSpot(14),
                ]
            ),
            Match(
                [
                    SeedMatchSpot(4),
                    SeedMatchSpot(5),
                    SeedMatchSpot(12),
                    SeedMatchSpot(13),
                ]
            ),
        ],
        leaderboard_type=LeaderboardType.BRACKET,
        config=round_config,
        qualifier=qualifier,
    )


def get_round_2(
    start_date: datetime, end_date: datetime, round_config: RoundConfig
) -> Round:
    return Round(
        name="Semi Finals",
        start_date=start_date,
        end_date=end_date,
        matches=[
            Match(
                [
                    MatchParticipantMatchSpot(0, 0, 1),
                    MatchParticipantMatchSpot(0, 1, 2),
                    MatchParticipantMatchSpot(0, 2, 2),
                    MatchParticipantMatchSpot(0, 3, 1),
                ]
            ),
            Match(
                [
                    MatchParticipantMatchSpot(0, 0, 2),
                    MatchParticipantMatchSpot(0, 1, 1),
                    MatchParticipantMatchSpot(0, 2, 1),
                    MatchParticipantMatchSpot(0, 3, 2),
                ]
            ),
        ],
        leaderboard_type=LeaderboardType.BRACKET,
        config=round_config,
    )


def get_round_3(
    start_date: datetime, end_date: datetime, round_config: RoundConfig
) -> Round:
    return Round(
        name="Grand Final",
        start_date=start_date,
        end_date=end_date,
        matches=[
            Match(
                [
                    MatchParticipantMatchSpot(1, 0, 1),
                    MatchParticipantMatchSpot(1, 0, 2),
                    MatchParticipantMatchSpot(1, 1, 1),
                    MatchParticipantMatchSpot(1, 1, 2),
                ]
            )
        ],
        leaderboard_type=LeaderboardType.BRACKET,
        config=round_config,
    )


def create_event() -> int:
    """
    Creates a new delta bracket event starting at the next Saturday 7:00pm UTC.

    :returns: Registered event ID of the event.
    """
    auth = os.getenv(UBI_AUTH)
    event_name = os.getenv(EVENT_NAME)
    club_id = os.getenv(CLUB_ID)
    campaign_id = os.getenv(CAMPAIGN_ID)

    # Get the map pool
    campaign_playlist = Campaign(club_id, campaign_id, auth)._playlist
    map_pool = [Map(campaign_map._uuid) for campaign_map in campaign_playlist]

    # Create the event at the upcoming Saturday 7:00pm UTC
    start_time = get_event_start()

    # Qualifier 7:00 - 7:30
    qualifier = get_qualifier(start_time, start_time + timedelta(minutes=30), map_pool)

    # Round 1 7:35 - 8:05
    round_1 = get_round_1(
        start_time + timedelta(minutes=35),
        start_time + timedelta(minutes=65),
        get_round_config(2, map_pool),
        qualifier,
    )

    # Round 2 8:10 - 8:40
    round_2 = get_round_2(
        start_time + timedelta(minutes=70),
        start_time + timedelta(minutes=100),
        get_round_config(2, map_pool),
    )

    # Round 3 8:45 - 9:15
    round_3 = get_round_3(
        start_time + timedelta(minutes=105),
        start_time + timedelta(minutes=135),
        get_round_config(3, map_pool),
    )

    event = Event(
        name=event_name,
        club_id=club_id,
        rounds=[round_1, round_2, round_3],
        description="Project Delta presents an automatically hosted weekly event every Saturday 7:00pm UTC. Join the discord: https://discord.gg/Nj2rDjqQPh",
    )
    event.post(auth)
