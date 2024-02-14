import json
import requests

from s3 import get_discord_webhook_url_from_secrets


def notify_event() -> None:
    """
    Sends notification to discord that an event is starting soon.
    """
    message = '<@&1207201665279860756> Pan-American of the Day will be starting soon! Join "NCSA Trackmania" Club and join "PAOTD" even to join!'
    requests.post(
        url=get_discord_webhook_url_from_secrets(),
        data=json.dumps({"content": message}),
        headers={"Content-Type": "application/json"},
    )
