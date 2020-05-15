"""Utility functions."""
import logging
from pathlib import Path
from typing import List

LOGGER = logging.getLogger(__name__)


def load_words(filename: str) -> List[str]:
    """Load a list of words from a file."""
    path = Path(filename)
    with path.open() as fh:
        words = fh.read().split("\n")
    LOGGER.info(f"Loaded {len(words)} words.")
    return words
