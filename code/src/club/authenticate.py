import requests


def authenticate(service: str, auth: str) -> str:
    """
    Authenticates with Nadeo Club Services and returns an access token.
    
    :param service: Audience (e.g. "NadeoClubServices", "NadeoLiveServices")
    :param auth: Authorization (e.g. "Basic <user:pass base 64>")
    :return: Authorization token
    """
    url = "https://public-ubiservices.ubi.com/v3/profiles/sessions"
    headers = {
        "Content-Type": "application/json",
        "Ubi-AppId": "86263886-327a-4328-ac69-527f0d20a237",
        "Authorization": auth,
        "User-Agent": "https://github.com/Nixotica/AutoEvents", 
    }
    print(requests.post(url, headers=headers))
    result = requests.post(url, headers=headers).json()
    print('result', result)

    url = "https://prod.trackmania.core.nadeo.online/v2/authentication/token/ubiservices"
    ticket = result["ticket"]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"ubi_v1 t={ticket}"
    }
    body = {
        "audience": service
    }
    result = requests.post(url, headers=headers, json=body)
    return result.json()["accessToken"]