from datetime import datetime
import json
import os
from typing import List, Optional
import requests
from src.constants import CREATE_COMP_URL

from src.api import authenticate

from src.api.structure.round.round import Round


class Event:
    def __init__(
        self,
        name: str,
        club_id: int,
        rounds: List[Round],
        description: str = None,
        registration_start_date: datetime = None,
        registration_end_date: datetime = None,
    ):
        self._name = name
        self._club_id = club_id
        self._rounds = rounds
        self._description = description
        self._registration_start_date = registration_start_date
        self._registration_end_date = registration_end_date

    def post(self, auth: str) -> None:
        """
        Posts the event with the given structure.

        :param auth: The authorization token for Ubisoft (e.g. "Basic <user:pass base 64>").
        """
        token = authenticate("NadeoClubServices", auth)
        response = requests.post(
            url=CREATE_COMP_URL,
            headers={"Authorization": "nadeo_v1 t=" + token},
            json=self.get_event_json(),
        ).json()
        self._registered_id = response["competition"]["id"]

    def get_event_json(self) -> json:
        pass

    def registered_id(self) -> Optional[int]:
        """
        Returns the ID this event is registered under in Nadeo's database. This can be useful
        for grabbing information about match progress or tearing down the event after its completion.
        """
        return self._registered_id
