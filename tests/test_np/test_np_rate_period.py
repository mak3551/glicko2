from glicko2.glicko2_np.glicko2_np import Glicko2_np
from glicko2 import WIN, LOSS, DRAW, rate_period, Player, Rating
from glicko2.rate_period import _get_series_of_player
from datetime import date
import math
import pytest

# allowable error (because sometimes float calculation is slightly incorrect)
ALLOWABLE: float = 0.001


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
    p_e: Player = Player(5, Rating(1450, 10, 0.08))
    player_list: list[Player] = [p_a, p_b, p_c, p_d, p_e]
    matches: list[tuple[Player, Player, float]] = [
        (p_a, p_b, WIN),
        (p_a, p_c, LOSS),
        (p_c, p_d, WIN),
        (p_d, p_a, DRAW),
    ]
    system: Glicko2_np = Glicko2_np(tau=1.2)
    match_date: date = date(2000, 6, 1)
    player_list = rate_period(matches, player_list, system, match_date)
    # p_a : r=1431.185, RD=157.209, sigma=0.030
    # p_b : r=1565.848, RD=98.416, sigma=0.070
    # p_c : r=1261.414, RD=40.690, sigma=0.050
    # p_d : r=1295.873, RD=243.477, sigma=0.060
    # p_e : r=1450.000, RD=17.121, sigma=0.080
    assert len(player_list) == 5
    assert (
        player_list[0].id == 1
        and assess_value(player_list[0].rating.r, 1431.185)
        and assess_value(player_list[0].rating.RD, 157.209)
        and assess_value(player_list[0].rating.sigma, 0.030)
        and len(player_list[0].rating_history) == 1
        and player_list[0].rating_history[0][0] == date(2000, 6, 1)
        and player_list[0].rating_history[0][1] == player_list[0].rating
    )
    assert (
        player_list[1].id == 2
        and assess_value(player_list[1].rating.r, 1565.848)
        and assess_value(player_list[1].rating.RD, 98.416)
        and assess_value(player_list[1].rating.sigma, 0.070)
        and len(player_list[1].rating_history) == 1
        and player_list[1].rating_history[0][0] == date(2000, 6, 1)
        and player_list[1].rating_history[0][1] == player_list[1].rating
    )
    assert (
        player_list[2].id == 3
        and assess_value(player_list[2].rating.r, 1261.414)
        and assess_value(player_list[2].rating.RD, 40.690)
        and assess_value(player_list[2].rating.sigma, 0.050)
        and len(player_list[2].rating_history) == 1
        and player_list[2].rating_history[0][0] == date(2000, 6, 1)
        and player_list[2].rating_history[0][1] == player_list[2].rating
    )
    assert (
        player_list[3].id == 4
        and assess_value(player_list[3].rating.r, 1295.873)
        and assess_value(player_list[3].rating.RD, 243.477)
        and assess_value(player_list[3].rating.sigma, 0.060)
        and len(player_list[3].rating_history) == 1
        and player_list[3].rating_history[0][0] == date(2000, 6, 1)
        and player_list[3].rating_history[0][1] == player_list[3].rating
    )
    assert (
        player_list[4].id == 5
        and assess_value(player_list[4].rating.r, 1450.000)
        and assess_value(player_list[4].rating.RD, 17.121)
        and assess_value(player_list[4].rating.sigma, 0.080)
        and len(player_list[4].rating_history) == 1
        and player_list[4].rating_history[0][0] == date(2000, 6, 1)
        and player_list[4].rating_history[0][1] == player_list[4].rating
    )

    print(player_list)
