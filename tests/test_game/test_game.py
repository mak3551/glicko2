import csv
import json
import math
from datetime import date
from timeit import timeit
from typing import Any

from glicko2 import game_rate_calculate

SAMPLE_CSV_FILE = "tests/test_game/sample.csv"
SAMPLE_RESULT_JSON_FILE = "tests/test_game/sample_result.json"

ALLOWABLE: float = 0.001


def assess_value(value: float, ref: float) -> bool:
    """
    It assesses if result value almost equals to reference value.
    """
    return math.fabs(value - ref) < ALLOWABLE


def assess_element(element_1: Any, element_2: Any) -> bool:
    """
    It compares two element. If element is list, dict or tuple, do recursive comparison.

    If an element is float, use assess_value() function to compare,
    and allows ALLOWABLE error.
    """
    if type(element_1) is not type(element_2):
        return False
    if isinstance(element_1, float):
        return assess_value(element_1, element_2)
    if isinstance(element_1, tuple | list):
        if len(element_1) != len(element_2):
            return False
        return all(assess_element(element_1[i], element_2[i]) for i in range(len(element_1)))
    if isinstance(element_1, dict):
        if len(element_1) != len(element_2):
            return False
        return all(assess_element(element_1[key], element_2[key]) for key in element_1)
    return bool(element_1 == element_2)


def _get_sample_data() -> list[tuple[str | date, str, str, float]]:
    sample_data: list[tuple[str | date, str, str, float]] = []
    with open(SAMPLE_CSV_FILE) as f:
        reader = csv.reader(f)
        for row in reader:
            sample_data.append((row[0], row[1], row[2], float(row[3])))
    return sample_data


def test_game_rate_calculate() -> None:
    sample_data: list[tuple[str | date, str, str, float]] = _get_sample_data()
    game_player_list = game_rate_calculate(sample_data, per_days=60)
    check_game_player = game_player_list.name_player_dict["FDVCHJg"]
    """
    GamePlayer(name='FDVCHJg', player=Player(unique_id=1, rating=Rating(r=1411.107707353713,
    rd=134.6010932313071, sigma=0.05997984243593714), rating_history=[(datetime.date(2000, 3, 5),
    Rating(r=1500.0, rd=181.34877960445007, sigma=0.05999027675029494)), (datetime.date(2000, 5, 5),
    Rating(r=1411.107707353713, rd=134.6010932313071, sigma=0.05997984243593714))]),
    first_mach_date=datetime.date(2000, 1, 2))
    """
    assert assess_value(check_game_player.player.rating.r, 1411.107)
    assert assess_value(check_game_player.player.rating.rd, 134.601)
    assert assess_value(check_game_player.player.rating.sigma, 0.0599)
    with open(SAMPLE_RESULT_JSON_FILE) as f:
        sample_result = json.load(f)
    assert assess_element(json.loads(game_player_list.dump_json()), sample_result)


def benchmark() -> None:
    print(
        timeit(
            "game_rate_calculate(sample_data, per_days=60,rating_system=system)",
            setup="from glicko2 import Glicko2Np;from tests.test_game.test_game import _get_sample_data, game_rate_calculate; \
                sample_data = _get_sample_data();system=Glicko2Np()",
            number=10000,
        )
    )
    print(
        timeit(
            "game_rate_calculate(sample_data, per_days=60,rating_system=system)",
            setup="from glicko2 import Glicko2;from tests.test_game.test_game import _get_sample_data,game_rate_calculate; \
                sample_data = _get_sample_data();system=Glicko2()",
            number=10000,
        )
    )
