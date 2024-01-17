from delta_bracket_v1.handler import delta_bracket_v1_handler
from pan_american_of_the_day.handler import pan_american_of_the_day_handler


def handler(event, context):
    """
    Top level lambda handler to dispatch to other handlers per event. The "event_name" event can be one of the following:

    1. delta_bracket_v1
    2. paotd
    """

    event_name = event["event_name"]
    if event_name == "delta_bracket_v1":
        return delta_bracket_v1_handler(event, context)
    elif event_name == "paotd":
        return pan_american_of_the_day_handler(event, context)
    else:
        raise Exception(
            f"Invalid event name {event_name}, choose one of (delta_bracket_v1)"
        )
