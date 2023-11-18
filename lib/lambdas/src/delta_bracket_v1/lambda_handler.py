def handler(event, context):
    """
    Takes in different events from eventbridge and designates logic accordingly. The event can be one of the following:

    1. Create qualifying event
    2. Create bracket event(s)
    3. Delete qualifying event
    4. Delete bracket event(s)
    """

    action = event["action"]
    if action == "create_qualifier":
        pass
    elif action == "create_brackets":
        pass
    elif action == "delete_qualifier":
        pass
    elif action == "delete_brackets":
        pass
    else:
        raise Exception(
            f"Invalid event action {action}, choose one of (create_qualifier, create_brackets, delete_qualifier, delete_brackets)"
        )
