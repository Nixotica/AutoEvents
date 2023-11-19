import os
from lib.lambdas.src.nadeo_event_api.src.api.authenticate import authenticate
from lib.lambdas.src.nadeo_event_api.src.api.enums import NadeoService
from lib.lambdas.src.nadeo_event_api.src.api.structure.event import Event
from lib.lambdas.src.nadeo_event_api.src.environment import UBI_AUTH


def delete_event(event_id: int):
    auth = authenticate(NadeoService.CLUB, os.getenv(UBI_AUTH))
    Event.delete_from_id(auth, event_id)
