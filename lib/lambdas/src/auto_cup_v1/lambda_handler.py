def handler(event, context):
    """
    Takes in different events from eventbridge and designates logic accordingly. The event can be one of the following:

    1. Notify of upcoming auto cup in the discord
    2. Create auto cup
    3. Delete auto cup
    """

    action = event["action"]

    if action == "create":
        # Create logic
        pass
    elif action == "notify":
        # Notify logic
        pass
    elif action == "delete":
        # Delete logic
        pass
    else:
        raise Exception(
            f"Invalid event action {action}, choose one of (create, notify, delete)"
        )
