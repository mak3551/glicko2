import csv
import math
from datetime import date

from glicko2.game_player import game_rate_calculate

SAMPLE_CSV_FILE = "tests/test_game/sample.csv"


ALLOWABLE: float = 0.005


def assess_value(value: float, ref: float) -> bool:
    """
    It assesses if result value almost equals to reference value.
    """
    return math.fabs(value - ref) < ALLOWABLE


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
