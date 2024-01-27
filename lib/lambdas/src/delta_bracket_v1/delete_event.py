import os
from nadeo_event_api.api.authenticate import UbiTokenManager
from nadeo_event_api.api.enums import NadeoService
from nadeo_event_api.api.structure.event import Event

from pan_american_of_the_day.environment import UBI_AUTH
from s3 import get_ubi_auth_from_secrets


def delete_event(event_id: int):
    # During integration tests in codecatalyst or env, we already have auth
    auth = os.getenv(UBI_AUTH)
    if auth is None:
        # Get ubi auth from s3, then force instantiate it so that event creation will use it.
        auth = get_ubi_auth_from_secrets()
    UbiTokenManager().authenticate(NadeoService.CLUB, auth)
    UbiTokenManager().authenticate(NadeoService.LIVE, auth)

    Event.delete_from_id(event_id)
