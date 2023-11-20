from enum import Enum


class LeaderboardType(Enum):
    """
    The leaderboard type for a round. Determines how scoring the round works.
    """

    BRACKET = "BRACKET"
    SUMSCORE = "SUMSCORE"
    SUM = "SUM"

    # TODO support more leaderboard types


class ScriptType(Enum):
    """
    The script type for a round. Determines the gamemode which will be played.
    """

    CUP = "TrackMania/TM_Cup_Online.Script.txt"
    TIME_ATTACK = "TrackMania/TM_TimeAttack_Online.Script.txt"

    # TODO support more script types


class PluginType(Enum):
    """
    The plugin type for a round. I'm actually not sure what other types there are.
    """

    EMPTY = ""
    CLUB = "server-plugins/Club/ClubPlugin.Script.txt"


class SpotType(Enum):
    """
    The stop type for a match. Determines how players are seeded in the match.
    """

    QUALIFICATION = "round_challenge_participant"
    SEED = "competition_participant"
    COMPETITION = "competition_leaderboard"
    MATCH = "match_participant"


class AutoStartMode(Enum):
    """
    The atuo start mode for a round. Determines the condition for when the round starts.
    """

    DELAY = "delay"

    # TODO support more modes
