from glicko2.rate_period import _get_series_of_player
from glicko2.glicko2 import WIN, LOSS, DRAW
from glicko2.player import Player


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
