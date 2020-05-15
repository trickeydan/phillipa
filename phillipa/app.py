import os

from phillipa.logging import logger_setup
from phillipa.utils import load_words
from phillipa.phillipa import PhillipaBot


def app():
    logger_setup()
    good = load_words("good.txt")
    bad = load_words("bad.txt")
    client = PhillipaBot(good, bad)
    token = os.environ.get('DISCORD_TOKEN', "NzEwMjMyOTg0NTk0MTUzNDcz.XrxgtA.IhI32vh8JZtlzWqCGQER_nRGzyY")
    client.run(token)