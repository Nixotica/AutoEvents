import json
import requests


def post_discord_message(webhook_url: str, message: str) -> None:
    """
    Posts a message to a discord channel using the given webhook.

    :param webhook_url: The webhook receiving the message
    :param message: The message to send
    """
    requests.post(
        url=webhook_url,
        data=json.dumps({"content": message}),
        headers={"Content-Type": "application/json"},
    )
