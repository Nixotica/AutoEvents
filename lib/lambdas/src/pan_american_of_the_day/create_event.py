from datetime import datetime, timedelta
import json
import os
import random
from typing import List
import pytz
from nadeo_event_api.api.structure.event import Event
from nadeo_event_api.api.authenticate import UbiTokenManager
from nadeo_event_api.api.enums import NadeoService
from nadeo_event_api.api.club.campaign import Campaign
from nadeo_event_api.api.structure.maps import Map
from nadeo_event_api.api.structure.round.qualifier import Qualifier, QualifierConfig
from nadeo_event_api.api.structure.enums import LeaderboardType, ScriptType, PluginType
from nadeo_event_api.api.structure.round.round import Round, RoundConfig
from nadeo_event_api.api.structure.enums import AutoStartMode
from nadeo_event_api.api.structure.round.match import Match
from nadeo_event_api.api.structure.round.match_spot import SeedMatchSpot
from nadeo_event_api.api.structure.settings.script_settings import (
    TimeAttackScriptSettings,
    CupScriptSettings,
    BaseScriptSettings,
)
from nadeo_event_api.api.structure.settings.plugin_settings import (
    ClassicPluginSettings,
    QualifierPluginSettings,
)
from s3 import get_ubi_auth_from_secrets

from pan_american_of_the_day.environment import (
    CAMPAIGN_ID,
    EVENT_CLUB_ID,
    EVENT_NAME,
    MAPS_CLUB_ID,
    UBI_AUTH,
)
from datetime import timedelta


def get_qualifier(
    start_date: datetime, end_date: datetime, map_pool: List[Map]
) -> Qualifier:
    return Qualifier(
        name="Qualifier",
        start_date=start_date,
        end_date=end_date,
        leaderboard_type=LeaderboardType.SUMSCORE,
        config=QualifierConfig(
            map_pool=map_pool,
            script=ScriptType.TIME_ATTACK,
            script_settings=TimeAttackScriptSettings(
                time_limit=300,
            ),
            plugin_settings=QualifierPluginSettings(
                use_playlist_complete=True,
            ),
            plugin=PluginType.CLUB,
        ),
    )


def get_round(
    start_date: datetime, end_date: datetime, qualifier: Qualifier, map_pool: List[Map]
) -> Round:
    return Round(
        name="PAOTD",
        start_date=start_date,
        end_date=end_date,
        qualifier=qualifier,
        config=RoundConfig(
            map_pool=map_pool,
            script=ScriptType.CUP,
            script_settings=CupScriptSettings(
                base_script_settings=BaseScriptSettings(
                    warmup_duration=75,
                    warmup_number=1,
                ),
                finish_timeout=15,
                number_of_winners=1,
                points_limit=120,
                rounds_per_map=4,
            ),
            plugin_settings=ClassicPluginSettings(
                auto_start_mode=AutoStartMode.DELAY,
                auto_start_delay=120,
            ),
            max_players=64,
            plugin=PluginType.CLUB,
        ),
        matches=[Match([SeedMatchSpot(x) for x in range(1, 65)])],
    )


def get_event_start() -> datetime:
    tz_paris = pytz.timezone("Europe/Paris")
    tomorrow = datetime.now(tz_paris) + timedelta(days=1)
    one_hour_after_cotn = tomorrow.replace(hour=4, minute=0, second=0)
    return one_hour_after_cotn.astimezone(pytz.utc).replace(tzinfo=None)


def create_event() -> Event:
    """
    Creates a new paotd event starting tomorrow at 4:00am CET/CEST (1 hour after COTN).

    :returns: The event.
    """
    event_name = os.getenv(EVENT_NAME)
    event_club_id = os.getenv(EVENT_CLUB_ID)
    maps_club_id = os.getenv(MAPS_CLUB_ID)
    campaign_id = os.getenv(CAMPAIGN_ID)

    # During integration tests in codecatalyst or env, we already have auth
    auth = os.getenv(UBI_AUTH)
    if auth is None:
        # Get ubi auth from s3, then force instantiate it so that event creation will use it.
        auth = get_ubi_auth_from_secrets()
    UbiTokenManager().authenticate(NadeoService.CLUB, auth)
    UbiTokenManager().authenticate(NadeoService.LIVE, auth)

    # Get a random map from the campaign
    campaign_playlist = Campaign(maps_club_id, campaign_id)._playlist
    random_4_maps = []
    for i in range(0, 4):
        random_4_maps.append(Map(random.choice(campaign_playlist)._uuid))

    # Create registration at now plus some offset so it's not in the past
    registration_start = datetime.utcnow() + timedelta(minutes=1)

    # Create the event at the upcoming 4:00am CET/CEST
    start_time = get_event_start()

    # Qualifier 4:00am - 4:05am
    qualifier = get_qualifier(
        start_time, start_time + timedelta(minutes=6), [random_4_maps[0]]
    )

    # Rounds mode 4:08am - 5:00am
    rounds = get_round(
        start_time + timedelta(minutes=8),
        start_time + timedelta(minutes=60),
        qualifier,
        random_4_maps,
    )

    # Event
    event = Event(
        name=event_name,
        club_id=event_club_id,
        registration_start_date=registration_start,
        registration_end_date=qualifier._end_date,
        rounds=[rounds],
        description="This is a Pan-American daily rounds event on the active NCSA competitive map pool! It is automatically hosted every night 1 hour after COTN. Join the discord: $lhttps://discord.gg/pj9C5znHzf",
    )
    event.post()
    return event
