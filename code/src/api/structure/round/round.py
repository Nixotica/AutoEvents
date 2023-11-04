from datetime import datetime
from typing import List
from src.constants import NADEO_DATE_FMT
from src.api.structure.round.match import Match
from src.api.structure.round.qualifier import Qualifier
from src.api.structure.enums import LeaderboardType, PluginType, ScriptType
from src.api.structure.maps import Map
from src.api.structure.settings import PluginSettings, ScriptSettings
import json


class RoundConfig:
    def __init__(
        self,
        map_pool: List[Map],
        script: ScriptType,
        max_players: int,
        max_spectators: int = None,
        plugin: PluginType = None,
        script_settings: ScriptSettings = None,
        plugin_settings: PluginSettings = None,
        password: str = None,
    ):
        self._map_pool = map_pool
        self._script = script
        self._max_players = max_players
        self._max_spectators = max_spectators
        self._plugin = plugin
        self._script_settings = script_settings
        self._plugin_settings = plugin_settings
        self._password = password


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

    def has_qualifier(self) -> bool:
        return self._qualifier is not None

    def as_jsonable_dict(self) -> dict:
        """
        Returns the round as a JSON-able dictionary.
        """
        with open("templates/round_template.json", "r") as template_file:
            template_json = json.load(template_file)
        template_json["name"] = self._name
        template_json["startDate"] = self._start_date.strftime(NADEO_DATE_FMT)
        template_json["endDate"] = self._end_date.strftime(NADEO_DATE_FMT)
        template_json["matches"] = [match.as_jsonable_dict() for match in self._matches]
        template_json["nbMatches"] = len(self._matches)
        template_json["leaderboardType"] = self._leaderboard_type
        template_json["config"] = self._config.as_jsonable_dict()
        template_json["config"]["name"] = self._name
        if self._qualifier is not None:
            template_json["qualifier"] = self._qualifier.as_jsonable_dict()
        return template_json
