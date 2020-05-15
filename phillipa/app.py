import logging
import os

from phillipa.utils import load_words
from phillipa.phillipa import PhillipaBot


def app():
    logging.info("Starting Phillipa")
    good = load_words("good.txt")
    bad = load_words("bad.txt")
    client = PhillipaBot(good, bad)
    token = os.environ.get('DISCORD_TOKEN', "NzEwMjMyOTg0NTk0MTUzNDcz.XrxgtA.IhI32vh8JZtlzWqCGQER_nRGzyY")
    client.run(token)