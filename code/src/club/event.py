import os
import requests
from code.src.constants import CREATE_COMP_URL

from code.src.club import authenticate


class Event:
    """
    A generic event with a valid structure for Nadeo-supported Events.
    TODO: Create structure class with params constructing the payload, and use that here.
    """

    def __init__(self, name: str, structure: dict):
        self._structure = structure

    def post(self, auth: str) -> str:
        """
        Posts the event with the given structure.

        :param auth: The authorization token for Ubisoft (e.g. "Basic <user:pass base 64>").
        :return: The competition ID
        """
        token = authenticate("NadeoClubServices", auth)
        response = requests.post(
            url=CREATE_COMP_URL,
            headers={"Authorization": "nadeo_v1 t=" + token},
            json=self._structure,
        ).json()
        return response["competition"]["id"]
