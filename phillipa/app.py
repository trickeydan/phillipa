"""Phillipa Application."""
import os

from phillipa.logging import logger_setup
from phillipa.phillipa import PhillipaBot
from phillipa.utils import load_words


def app() -> None:
    """Main Phillipa Application."""
    logger_setup()
    good = load_words("good.txt")
    bad = load_words("bad.txt")
    client = PhillipaBot(good, bad)
    token = os.environ.get('DISCORD_TOKEN')
    client.run(token)
