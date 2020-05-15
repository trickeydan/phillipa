from pathlib import Path

def load_words(filename):
    path = Path(filename)
    with path.open() as fh:
        return fh.read().split("\n")