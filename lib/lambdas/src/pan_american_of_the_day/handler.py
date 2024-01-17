from s3 import get_latest_event_id_from_s3, upload_event_id_to_s3
from pan_american_of_the_day.delete_event import delete_event
from pan_american_of_the_day.create_event import create_event


def pan_american_of_the_day_handler(event, context):
    """
    Takes in different events from eventbridge and designates logic accordingly. The "action" event can be one of the following:

    1. Create event
    2. Delete event
    """

    action = event["action"]
    if action == "create":
        event = create_event()
        upload_event_id_to_s3(event._registered_id)
    elif action == "delete":
        event_id = get_latest_event_id_from_s3()
        delete_event(event_id)
    else:
        raise Exception(
            f"Invalid event action {action}, choose one of (create, delete)"
        )
