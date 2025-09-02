import math
from datetime import date

from glicko2 import DRAW, LOSS, WIN, Glicko2Np, Player, Rating, rate_period

# allowable error (because sometimes float calculation is slightly incorrect)
ALLOWABLE: float = 0.001


def assess_value(value: float, ref: float) -> bool:
    """
    It assesses if result value almost equals to reference value.
    """
    return math.fabs(value - ref) < ALLOWABLE


def test_rate_period() -> None:
    p_a: Player = Player(1, Rating(1400, 200, 0.03))
    p_b: Player = Player(2, Rating(1600, 100, 0.07))
    p_c: Player = Player(3, Rating(1250, 40, 0.05))
    p_d: Player = Player(4, Rating(1700, 300, 0.06))
    p_e: Player = Player(5, Rating(1450, 10, 0.08))
    player_list: list[Player] = [p_a, p_b, p_c, p_d, p_e]
    len_old_player_list: int = len(player_list)
    matches: list[tuple[Player, Player, float]] = [
        (p_a, p_b, WIN),
        (p_a, p_c, LOSS),
        (p_c, p_d, WIN),
        (p_d, p_a, DRAW),
    ]
    system: Glicko2Np = Glicko2Np(tau=1.2)
    match_date: date = date(2000, 6, 1)
    player_list = rate_period(matches, player_list, system, match_date)
    # p_a : r=1431.185, rd=157.209, sigma=0.030
    # p_b : r=1565.848, rd=98.416, sigma=0.070
    # p_c : r=1261.414, rd=40.690, sigma=0.050
    # p_d : r=1295.873, rd=243.477, sigma=0.060
    # p_e : r=1450.000, rd=17.121, sigma=0.080
    assert len(player_list) == len_old_player_list
    assert player_list[0].unique_id == 1
    assert assess_value(player_list[0].rating.r, 1431.185)
    assert assess_value(player_list[0].rating.rd, 157.209)
    assert assess_value(player_list[0].rating.sigma, 0.030)
    assert len(player_list[0].rating_history) == 1
    assert player_list[0].rating_history[0][0] == date(2000, 6, 1)
    assert player_list[0].rating_history[0][1] == player_list[0].rating

    assert player_list[1].unique_id == 2
    assert assess_value(player_list[1].rating.r, 1565.848)
    assert assess_value(player_list[1].rating.rd, 98.416)
    assert assess_value(player_list[1].rating.sigma, 0.070)
    assert len(player_list[1].rating_history) == 1
    assert player_list[1].rating_history[0][0] == date(2000, 6, 1)
    assert player_list[1].rating_history[0][1] == player_list[1].rating

    assert player_list[2].unique_id == 3
    assert assess_value(player_list[2].rating.r, 1261.414)
    assert assess_value(player_list[2].rating.rd, 40.690)
    assert assess_value(player_list[2].rating.sigma, 0.050)
    assert len(player_list[2].rating_history) == 1
    assert player_list[2].rating_history[0][0] == date(2000, 6, 1)
    assert player_list[2].rating_history[0][1] == player_list[2].rating

    assert player_list[3].unique_id == 4
    assert assess_value(player_list[3].rating.r, 1295.873)
    assert assess_value(player_list[3].rating.rd, 243.477)
    assert assess_value(player_list[3].rating.sigma, 0.060)
    assert len(player_list[3].rating_history) == 1
    assert player_list[3].rating_history[0][0] == date(2000, 6, 1)
    assert player_list[3].rating_history[0][1] == player_list[3].rating

    assert player_list[4].unique_id == 5
    assert assess_value(player_list[4].rating.r, 1450.000)
    assert assess_value(player_list[4].rating.rd, 17.121)
    assert assess_value(player_list[4].rating.sigma, 0.080)
    assert len(player_list[4].rating_history) == 1
    assert player_list[4].rating_history[0][0] == date(2000, 6, 1)
    assert player_list[4].rating_history[0][1] == player_list[4].rating
