from datetime import datetime
from typing import List
from nadeo_event_api.src.constants import NADEO_DATE_FMT
from nadeo_event_api.src.api.structure.round.match import Match
from nadeo_event_api.src.api.structure.round.qualifier import Qualifier
from nadeo_event_api.src.api.structure.enums import (
    LeaderboardType,
    PluginType,
    ScriptType,
)
from nadeo_event_api.src.api.structure.maps import Map
from nadeo_event_api.src.api.structure.settings import PluginSettings, ScriptSettings


class RoundConfig:
    def __init__(
        self,
        map_pool: List[Map],
        script: ScriptType,
        max_players: int,
        max_spectators: int = 32,
        plugin: PluginType = PluginType.EMPTY,
        script_settings: ScriptSettings = ScriptSettings(),
        plugin_settings: PluginSettings = PluginSettings(),
    ):
        self._map_pool = map_pool
        self._script = script
        self._max_players = max_players
        self._max_spectators = max_spectators
        self._plugin = plugin
        self._script_settings = script_settings
        self._plugin_settings = plugin_settings

    def as_jsonable_dict(self) -> dict:
        """
        Returns the round config as a JSON-able dictionary.
        """
        config = {}
        config["maps"] = [map._uuid for map in self._map_pool]
        config["script"] = self._script.value
        config["maxPlayers"] = self._max_players
        config["maxSpectators"] = self._max_spectators
        config["plugin"] = self._plugin.value
        config["pluginSettings"] = self._plugin_settings.as_jsonable_dict()
        config["scriptSettings"] = self._script_settings.as_jsonable_dict()
        return config


class Round:
    def __init__(
        self,
        name: str,
        start_date: datetime,
        end_date: datetime,
        matches: List[Match],
        leaderboard_type: LeaderboardType,
        config: RoundConfig,
        qualifier: Qualifier = None,
    ):
        self._name = name
        self._start_date = start_date
        self._end_date = end_date
        self._matches = matches
        self._leaderboard_type = leaderboard_type
        self._config = config
        self._qualifier = qualifier
        self._team_leaderboard_type = "TEAM_SCORE"  # TODO figure out what this is

    def as_jsonable_dict(self) -> dict:
        """
        Returns the round as a JSON-able dictionary.
        """
        round = {}
        round["name"] = self._name
        round["startDate"] = self._start_date.strftime(NADEO_DATE_FMT)
        round["endDate"] = self._end_date.strftime(NADEO_DATE_FMT)
        round["nbMatches"] = 0  # It always starts with zero by default
        round["leaderboardType"] = self._leaderboard_type.value
        round["config"] = self._config.as_jsonable_dict()
        round["config"]["name"] = self._name
        round["qualifier"] = (
            self._qualifier.as_jsonable_dict() if self._qualifier else None
        )
        round["teamLeaderboardType"] = self._team_leaderboard_type
        return round
