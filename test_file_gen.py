import time
from datetime import datetime
from pathlib import Path
from random import randint


def ensure_path_exists(path: Path) -> None:
    if not path.exists():
        path.mkdir(parents=True)


def get_random_location() -> str:
    """
    Returns a random location from the list of locations.
    """
    locations = ["London", "Sydney", "New York", "Tokyo", "Paris", "Berlin"]
    return locations[randint(0, len(locations) - 1)]


def get_random_topic() -> str:
    """
    Returns a random topic from the list of topics.
    """
    topics = ["we", "are", "the", "knights", "who", "say", "ni"]
    return topics[randint(0, len(topics) - 1)]


def create_test_file() -> None:
    """
    Creates a test file in a random location with a random topic.
    """
    test_time = datetime.now().strftime("%Y/%M/%D/%H/%m")
    path = Path(f"test-files/{get_random_location()}/{test_time}")

    # We need to ensure that the path exists before we can create the file, however we don't want to create a
    # directory for the minutes, so we cut that off.
    ensure_path_exists(path.parent)

    with open(f"{path}-{get_random_topic()}.dat", "w") as f:
        f.write("This is a test file")


while True:
    create_test_file()
    time.sleep(randint(30, 100))
