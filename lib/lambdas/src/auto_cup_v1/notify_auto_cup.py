import os

from nadeo_event_api.api.discord.webhook import post_discord_message


def notify_auto_cup() -> None:
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    post_discord_message(
        webhook_url,
        '<@&1080011219043360819> Another edition of Auto Cup will be starting in 1 hour! Join "Auto Events" Club to play!',
    )
