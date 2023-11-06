import requests

from src.constants import NADEO_AUTH_URL, UBI_SESSION_URL


def authenticate(service: str, auth: str) -> str:
    """
    Authenticates with Nadeo Club Services and returns an access token.

    :param service: Audience (e.g. "NadeoClubServices", "NadeoLiveServices")
    :param auth: Authorization (e.g. "Basic <user:pass base 64>")
    :return: Authorization token
    """
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
    body = {"audience": service}
    result = requests.post(NADEO_AUTH_URL, headers=headers, json=body).json()
    return result["accessToken"]
