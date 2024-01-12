from nadeo_event_api.api.structure.event import Event


def delete_event(event_id: int):
    Event.delete_from_id(event_id)
