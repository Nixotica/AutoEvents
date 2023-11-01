from enum import Enum


def LeaderboardType(Enum):
    """
    The leaderboard type for a round. Determines how scoring the round works.
    """
    BRACKET = "BRACKET"
    SUMSCORE = "SUMSCORE"

    # TODO support more leaderboard types


def ScriptType(Enum):
    """
    The script type for a round. Determines the gamemode which will be played.
    """
    CUP = "TrackMania/TM_Cup_Online.Script.txt"

    # TODO support more script types


def PluginType(Enum):
    """
    The plugin type for a round. I'm actually not sure what other types there are.
    """
    CLUB = "server-plugins/Club/ClubPlugin.Script.txt"
