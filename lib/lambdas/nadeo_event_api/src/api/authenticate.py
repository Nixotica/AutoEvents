import os
import requests
from delta_bracket_v1.src.s3 import get_ubi_auth_from_secrets
from nadeo_event_api.src.environment import UBI_AUTH
from nadeo_event_api.src.api.enums import NadeoService

from nadeo_event_api.src.constants import NADEO_AUTH_URL, UBI_SESSION_URL


class UbiTokenManager:
    _instance = None
    _nadeo_live_token = None
    _nadeo_club_token = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UbiTokenManager, cls).__new__(cls)
        return cls._instance

    def authenticate(self, service: NadeoService) -> str:
        """
        Authenticates with the provided Nadeo service given authorization
        and returns an access token.

        :param service: Audience (e.g. "NadeoClubServices", "NadeoLiveServices")
        :return: Access token
        """
        env_auth = os.getenv(UBI_AUTH)
        auth = env_auth if env_auth else get_ubi_auth_from_secrets()
        headers = {
            "Content-Type": "application/json",
            "Ubi-AppId": "86263886-327a-4328-ac69-527f0d20a237",
            "Authorization": auth,
            "User-Agent": "https://github.com/Nixotica/AutoEvents",
        }
        result = requests.post(UBI_SESSION_URL, headers=headers).json()

        ticket = result["ticket"]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"ubi_v1 t={ticket}",
        }
        body = {"audience": service.value}
        result = requests.post(NADEO_AUTH_URL, headers=headers, json=body).json()
        return result["accessToken"]

    @property
    def nadeo_live_token(self) -> str:
        if self._nadeo_live_token is None:
            self._nadeo_live_token = self.authenticate(NadeoService.LIVE)
        return self._nadeo_live_token

    @property
    def nadeo_club_token(self) -> str:
        if self._nadeo_club_token is None:
            self._nadeo_club_token = self.authenticate(NadeoService.CLUB)
        return self._nadeo_club_token

    @nadeo_live_token.setter
    def nadeo_live_token(self, value):
        self._nadeo_live_token = value

    @nadeo_club_token.setter
    def nadeo_club_token(self, value):
        self._nadeo_club_token = value
