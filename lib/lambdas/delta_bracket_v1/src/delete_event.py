import os
from delta_bracket_v1.src.s3 import get_ubi_auth_from_secrets
from nadeo_event_api.src.api.authenticate import authenticate
from nadeo_event_api.src.api.enums import NadeoService
from nadeo_event_api.src.api.structure.event import Event


def delete_event(event_id: int):
    auth = authenticate(NadeoService.CLUB, get_ubi_auth_from_secrets())
    Event.delete_from_id(auth, event_id)
