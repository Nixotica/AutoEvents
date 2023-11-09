from enum import Enum


class NadeoService(Enum):
    """
    The Nadeo services to authenticate with.
    """

    CLUB = "NadeoClubServices"
    LIVE = "NadeoLiveServices"
