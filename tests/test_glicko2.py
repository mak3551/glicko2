# -*- coding: utf-8 -*-
from glicko2.glicko2 import Glicko2, WIN, LOSS, Rating
import math


ALLOWABLE: float = 0.01


def assess_value(value: float, ref: float) -> bool:
    """
    It assesses if result value almost equals to reference value.
    """
    return math.fabs(value - ref) < ALLOWABLE


def test_glickman_example() -> None:
    """
    This test uses example calculation in Mark Glickman's paper. https://www.glicko.net/glicko/glicko2.pdf
    """
    env: Glicko2 = Glicko2(tau=0.5)
    r1 = env.create_rating(1500, 200, 0.06)
    r2 = env.create_rating(1400, 30)
    r3 = env.create_rating(1550, 100)
    r4 = env.create_rating(1700, 300)
    rated: Rating = env.rate(r1, [(WIN, r2), (LOSS, r3), (LOSS, r4)])

    assert assess_value(rated.r, 1464.051)
    assert assess_value(rated.RD, 151.515)
    assert assess_value(rated.sigma, 0.05999)
    assert assess_value(env.expect_score(r1, r2), 0.639)
    assert assess_value(env.expect_score(r1, r3), 0.432)
    assert assess_value(env.expect_score(r1, r4), 0.303)
