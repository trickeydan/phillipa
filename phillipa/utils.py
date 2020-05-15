import logging
from pathlib import Path

LOGGER = logging.getLogger(__name__)

def load_words(filename):
    path = Path(filename)
    with path.open() as fh:
        words = fh.read().split("\n")
    LOGGER.info(f"Loaded {len(words)} words.")
    return words