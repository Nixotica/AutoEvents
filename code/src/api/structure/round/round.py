from datetime import datetime
from src.api.structure.round.qualifier import Qualifier

from src.api.structure.enums import LeaderboardType, PluginType, ScriptType

from src.api.structure.maps import MapPool

from src.api.structure.settings import PluginSettings, ScriptSettings


class RoundConfig:
    def __init__(
        self,
        num_matches: int,
        leaderboard_type: LeaderboardType,
        map_pool: MapPool,
        script: ScriptType,
        max_players: int,
        max_spectators: int = None,
        plugin: PluginType = None,
        script_settings: ScriptSettings = None,
        plugin_settings: PluginSettings = None,
        password: str = None,
    ):
        self._num_matches = num_matches
        self._leaderboard_type = leaderboard_type
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
        config: RoundConfig = None,
        qualifier: Qualifier = None,
    ):
        self._name = name
        self._start_date = start_date
        self._end_date = end_date
        self._config = config
        self._qualifier = qualifier

    def has_qualifier(self) -> bool:
        return self._qualifier is not None
