from glicko2.rate_period import rate_period, _get_series_of_player
from glicko2.glicko2 import WIN, LOSS, DRAW, Glicko2, Rating
from glicko2.player import Player
from datetime import date
import math
import pytest

ALLOWABLE: float = 0.005


def assess_value(value: float, ref: float) -> bool:
    """
    It assesses if result value almost equals to reference value.
    """
    return math.fabs(value - ref) < ALLOWABLE


def test_get_series_of_player() -> None:
    p_a: Player = Player(1)
    p_b: Player = Player(2)
    p_c: Player = Player(3)
    p_d: Player = Player(4)
    matches: list[tuple[Player, Player, float]] = [
        (p_a, p_b, WIN),
        (p_a, p_c, LOSS),
        (p_c, p_d, WIN),
        (p_d, p_a, DRAW),
    ]
    assert _get_series_of_player(matches, p_a) == [
        (WIN, p_b.rating),
        (LOSS, p_c.rating),
        (DRAW, p_d.rating),
    ]
    assert _get_series_of_player(matches, p_b) == [(LOSS, p_a.rating)]
    assert _get_series_of_player(matches, p_c) == [(WIN, p_a.rating), (WIN, p_d.rating)]
    assert _get_series_of_player(matches, p_d) == [
        (LOSS, p_c.rating),
        (DRAW, p_a.rating),
    ]
    invalid_matches: list[tuple[Player, Player, float]] = [
        (p_a, p_c, WIN),
        (p_b, p_b, WIN),
    ]
    with pytest.raises(RuntimeError):
        _get_series_of_player(invalid_matches, p_b)


def test_rate_period() -> None:
    p_a: Player = Player(1, Rating(1400, 200, 0.03))
    p_b: Player = Player(2, Rating(1600, 100, 0.07))
    p_c: Player = Player(3, Rating(1250, 40, 0.05))
    p_d: Player = Player(4, Rating(1700, 300, 0.06))
    # p_e: Player = Player(5, Rating(1450, 10, 0.08))
    player_list: list[Player] = [p_a, p_b, p_c, p_d]
    matches: list[tuple[Player, Player, float]] = [
        (p_a, p_b, WIN),
        (p_a, p_c, LOSS),
        (p_c, p_d, WIN),
        (p_d, p_a, DRAW),
    ]
    system: Glicko2 = Glicko2(tau=1.2)
    match_date: date = date(2000, 6, 1)
    player_list = rate_period(matches, player_list, system, match_date)
    # p_a : r=1431.185, RD=157.209, sigma=0.030
    # p_b : r=1565.848, RD=98.416, sigma=0.070
    # p_c : r=1261.414, RD=40.690, sigma=0.050
    # p_d : r=1295.873, RD=243.477, sigma=0.060
    # p_e : r=1450.000, RD=17.121, sigma=0.080
    print(player_list)
