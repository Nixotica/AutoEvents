import os
from delta_bracket_v1.handler import delta_bracket_v1_handler


def handler(event, context):
    """
    Top level lambda handler to dispatch to other handlers per event. The "event_name" event can be one of the following:

    1. Delta bracket v1
    """

    event_name = event["event"]
    if event_name == "delta_bracket_v1":
        return delta_bracket_v1_handler(event, context)
    else:
        raise Exception(
            f"Invalid event name {event_name}, choose one of (delta_bracket_v1)"
        )
