from datetime import datetime
import json
import os
from typing import List, Optional
import requests
from src.api.structure.round.spot_structure import SpotStructure
from src.constants import CREATE_COMP_URL, NADEO_DATE_FMT

from src.api import authenticate

from src.api.structure.round.round import Round


class Event:
    def __init__(
        self,
        name: str,
        club_id: int,
        rounds: List[Round],
        description: str = "",
        registration_start_date: datetime = None,
        registration_end_date: datetime = None,
    ):
        self._name = name
        self._club_id = club_id
        self._rounds = rounds
        self._description = description
        self._registration_start_date = registration_start_date
        self._registration_end_date = registration_end_date

        self._registered_id = None
        """ The ID this event is registered under in Nadeo's database. None if not registered. """

    def post(self, auth: str) -> None:
        """
        Posts the event with the given structure.

        :param auth: The authorization token for Ubisoft (e.g. "Basic <user:pass base 64>").
        """
        token = authenticate("NadeoClubServices", auth)
        response = requests.post(
            url=CREATE_COMP_URL,
            headers={"Authorization": "nadeo_v1 t=" + token},
            json=json.dumps(self._as_jsonable_dict()),
        ).json()
        self._registered_id = response["competition"]["id"]

    @staticmethod
    def delete(auth: str, event_id: int) -> None:
        """
        Deletes the event with the given ID.

        :param auth: The authorization token for Ubisoft (e.g. "Basic <user:pass base 64>").
        :param event_id: The ID of the event to delete.
        """
        pass

    def _as_jsonable_dict(self) -> dict:
        """
        Returns the event as a JSON-able dictionary.
        """
        event = {}
        event["name"] = self._name
        event["clubId"] = self._club_id
        event["description"] = self._description
        event["registrationStartDate"] = self._registration_start_date.strftime(
            NADEO_DATE_FMT
        )
        event["registrationEndDate"] = self._registration_end_date.strftime(
            NADEO_DATE_FMT
        )
        event["rounds"] = [round.as_jsonable_dict() for round in self._rounds]
        for i in range(len(self._rounds)):
            event["rounds"][i]["position"] = i
        event["rulesUrl"] = None
        event["spotStructure"] = SpotStructure(self._rounds).as_jsonable_dict()
        event["startDate"] = ""
        event["maxPlayers"] = 10000
        event["allowedZone"] = ""
        event["participantType"] = "PLAYER"
        return event
