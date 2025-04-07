from pathlib import Path


def clear_dir(curr_dir: Path) -> None:
    """
    Based on example in https://docs.python.org/3/library/pathlib.html#pathlib.Path.walk
    """

    if not curr_dir.is_dir():
        raise ValueError

    for parent, dirs, files in curr_dir.walk(top_down=False):
        for filename in files:
            (parent / filename).unlink()
        for dirname in dirs:
            (parent / dirname).rmdir()
