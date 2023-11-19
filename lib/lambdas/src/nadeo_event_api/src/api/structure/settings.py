import json
from src.api.structure.enums import AutoStartMode


# TODO add all these settings https://doc.trackmania.com/club/competition-tool/plugin-settings/
class PluginSettings:
    def __init__(
        self,
        auto_start_mode: AutoStartMode = AutoStartMode.DELAY,
        auto_start_delay: int = 600,
        pick_ban_start_auto: bool = False,
        pick_ban_order: str = "",
    ):
        self._auto_start_mode = auto_start_mode
        self._auto_start_delay = auto_start_delay
        self._pick_ban_start_auto = pick_ban_start_auto
        self._pick_ban_order = pick_ban_order

        # TODO make these configurable once I know what they mean
        self._ad_image_urls = ""
        self._enable_ready_manager = True
        self._use_auto_ready = True
        self._ready_start_ratio = 1
        self._message_timer = ""

    def as_jsonable_dict(self) -> dict:
        plugin_settings = {}
        plugin_settings["S_AdImageUrls"] = self._ad_image_urls
        plugin_settings["S_AutoStartMode"] = self._auto_start_mode.value
        plugin_settings["S_AutoStartDelay"] = self._auto_start_delay
        plugin_settings["S_PickBanStartAuto"] = self._pick_ban_start_auto
        plugin_settings["S_PickBanOrder"] = self._pick_ban_order
        plugin_settings["S_EnableReadyManager"] = self._enable_ready_manager
        plugin_settings["S_UseAutoReady"] = self._use_auto_ready
        plugin_settings["S_ReadyStartRatio"] = self._ready_start_ratio
        plugin_settings["S_MessageTimer"] = self._message_timer
        return plugin_settings


class QualifierPluginSettings:
    def __init__(
        self,
    ):
        # TODO make these configurable once I know what they mean
        self._ad_image_urls = ""
        self._message_timer = ""

    def as_jsonable_dict(self) -> dict:
        plugin_settings = {}
        plugin_settings["S_AdImageUrls"] = self._ad_image_urls
        plugin_settings["S_MessageTimer"] = self._message_timer
        return plugin_settings


# TODO add all these settings https://wiki.trackmania.io/en/dedicated-server/Usage/OfficialGameModesSettings
class ScriptSettings:
    def __init__(
        self,
        points_repartition: str = "",  # TODO make list and convert to string here
        points_limit: int = 100,
        finish_timeout: int = -1,
        rounds_per_map: int = 5,
        number_of_winners: int = 3,
        warmup_number: int = 1,
        warmup_duration: int = 120,
    ):
        self._points_repartition = points_repartition
        self._points_limit = points_limit
        self._finish_timeout = finish_timeout
        self._rounds_per_map = rounds_per_map
        self._number_of_winners = number_of_winners
        self._warmup_number = warmup_number
        self._warmup_duration = warmup_duration

    def as_jsonable_dict(self) -> dict:
        script_settings = {}
        script_settings["S_PointsRepartition"] = self._points_repartition
        script_settings["S_PointsLimit"] = self._points_limit
        script_settings["S_FinishTimeout"] = self._finish_timeout
        script_settings["S_RoundsPerMap"] = self._rounds_per_map
        script_settings["S_NbOfWinners"] = self._number_of_winners
        script_settings["S_WarmUpNb"] = self._warmup_number
        script_settings["S_WarmUpDuration"] = self._warmup_duration
        return script_settings


class QualifierScriptSettings:
    def __init__(
        self,
        time_limit: int = 300,
        warmup_number: int = 1,
        warmup_duration: int = 15,
        force_laps_number: int = 0,
    ):
        self._time_limit = time_limit
        self._warmup_number = warmup_number
        self._warmup_duration = warmup_duration
        self._force_laps_number = force_laps_number

    def as_jsonable_dict(self) -> dict:
        script_settings = {}
        script_settings["S_TimeLimit"] = self._time_limit
        script_settings["S_WarmUpNb"] = self._warmup_number
        script_settings["S_WarmUpDuration"] = self._warmup_duration
        script_settings["S_ForceLapsNb"] = self._force_laps_number
        return script_settings
