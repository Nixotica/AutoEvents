from datetime import datetime
from typing import List
import requests
from nadeo_event_api.src.api.enums import NadeoService
from nadeo_event_api.src.api.structure.round.spot_structure import SpotStructure
from nadeo_event_api.src.constants import (
    CREATE_COMP_URL,
    DELETE_COMP_URL_FMT,
    NADEO_DATE_FMT,
)

from nadeo_event_api.src.api.authenticate import authenticate

from nadeo_event_api.src.api.structure.round.round import Round


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

        self._registered_id = None
        """ The ID this event is registered under in Nadeo's database. None if not registered. """

    def post(self, auth: str) -> None:
        """
        Posts the event if valid.

        :param auth: The authorization token for Ubisoft (e.g. "Basic <user:pass base 64>").
        """
        if not self.valid():
            print("Event is not valid, and therefore will not post.")
            return

        token = authenticate(NadeoService.CLUB, auth)
        response = requests.post(
            url=CREATE_COMP_URL,
            headers={"Authorization": "nadeo_v1 t=" + token},
            json=self._as_jsonable_dict(),
        ).json()
        if "exception" in response:
            print("Failed to post event: ", response)
        self._registered_id = response["competition"]["id"]

    def delete(self, auth: str) -> None:
        """
        Deletes this event.

        :param auth: The authorization token for Ubisoft (e.g. "Basic <user:pass base 64>").
        """
        if not self._registered_id:
            print("Could not delete event since it hasn't been posted.")
            return
        token = authenticate(NadeoService.CLUB, auth)
        requests.post(
            url=DELETE_COMP_URL_FMT.format(self._registered_id),
            headers={"Authorization": "nadeo_v1 t=" + token},
        )
        self._registered_id = None

    @staticmethod
    def delete_from_id(auth: str, event_id: int) -> None:
        """
        Deletes the event with the given ID.

        :param auth: The authorization token for Ubisoft (e.g. "Basic <user:pass base 64>").
        :param event_id: The ID of the event to delete.
        """
        token = authenticate(NadeoService.CLUB, auth)
        requests.post(
            url=DELETE_COMP_URL_FMT.format(event_id),
            headers={"Authorization": "nadeo_v1 t=" + token},
        )

    """
    TODO Get the registered players from original competition (static method)
    get_participants_url = f"https://competition.trackmania.nadeo.club/api/competitions/{comp_id}/participants?offset=0&length=50"
    """

    def _as_jsonable_dict(self) -> dict:
        """
        Returns the event as a JSON-able dictionary.
        """
        event = {}
        event["name"] = self._name
        event["clubId"] = self._club_id
        event["description"] = self._description
        event["registrationStartDate"] = (
            self._registration_start_date.strftime(NADEO_DATE_FMT)
            if self._registration_start_date
            else None
        )
        event["registrationEndDate"] = (
            self._registration_end_date.strftime(NADEO_DATE_FMT)
            if self._registration_end_date
            else None
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

    def valid(self) -> bool:
        """
        Ensures that event is valid to post. This is because we get very little
        insight as to why the event is invalid from the response, so we need to check
        against what we know is allowed/disallowed.

        :returns: True if valid, False otherwise.
        """
        now = datetime.utcnow()
        if self._registration_start_date and self._registration_end_date:
            if now > self._registration_start_date or now > self._registration_end_date:
                print("Event registration must be later than current time.")
                return False
            if self._registration_start_date > self._registration_end_date:
                print("Event registration start must be before end.")
                return False
        elif self._registration_start_date or self._registration_end_date:
            print("Event registration start and end must be specified together.")
            return False

        if len(self._name) > 16:
            print("Event name is probably too long and will break.")
            return False

        # TODO check that all rounds, qualifiers, matches, etc are formed correctly (+ maps are real)

        # TODO check that club id belongs to authorized user

        return True
