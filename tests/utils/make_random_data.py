import csv
import pathlib
import random
import string
from datetime import date

MIN_DATE: date = date(2000, 1, 1)
MAX_DATE: date = date(2000, 6, 30)

MAX_NAME_LENGTH: int = 10
MIN_NAME_LENGTH: int = 3


def _random_date() -> date:
    max_date_ordinal: int = MAX_DATE.toordinal()
    min_date_ordinal: int = MIN_DATE.toordinal()
    random_ordinal = random.randint(min_date_ordinal, max_date_ordinal)
    return date.fromordinal(random_ordinal)


def _random_name_generate() -> str:
    name: str = ""
    name_length = random.randint(MIN_NAME_LENGTH, MAX_NAME_LENGTH)
    for _i in range(name_length):
        name += random.choice(string.ascii_letters)
    return name


def _random_name_set(set_size: int = 6) -> set[str]:
    name_set: set[str] = set()
    while len(name_set) < set_size:
        random_name: str = _random_name_generate()
        name_set.add(random_name)
    return name_set


def _random_result() -> float:
    return random.choice((0.0, 1.0))


def get_random_game_list(count: int = 50) -> list[tuple[str, str, str, float]]:
    name_set: set[str] = _random_name_set()
    game_list: list[tuple[str, str, str, float]] = []
    for _i in range(count):
        game_date: str = _random_date().isoformat()
        player_list: list[str] = random.sample(list(name_set), k=2)
        result: float = _random_result()
        game_list.append((game_date, player_list[0], player_list[1], result))
    return game_list


def make_random_data_file(output_file: str | pathlib.Path) -> None:
    random_data: list[tuple[str, str, str, float]] = get_random_game_list()
    with open(output_file, "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(random_data)
    return None
