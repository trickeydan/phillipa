"""Phillipa Application."""
import os

from phillipa.logging import logger_setup
from phillipa.phillipa import PhillipaBot


def app() -> None:
    """Main Phillipa Application."""
    logger_setup()
    client = PhillipaBot()
    token = os.environ.get("DISCORD_TOKEN")
    if token is not None:
        client.run(token)
    else:
        print("Missing token.")
