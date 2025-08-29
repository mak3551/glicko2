# -*- coding: utf-8 -*-
from glicko2.glicko2_np.glicko2_np import Glicko2_np
from glicko2 import WIN, LOSS, Rating
import math


ALLOWABLE: float = 0.001


def assess_value(value: float, ref: float) -> bool:
    """
    It assesses if result value almost equals to reference value.
    """
    return math.fabs(value - ref) < ALLOWABLE


def test_glickman_example() -> None:
    """
    This test uses example calculation in Mark Glickman's paper. https://www.glicko.net/glicko/glicko2.pdf
    """
    env: Glicko2_np = Glicko2_np(tau=0.5)
    r1 = env.create_rating(1500, 200, 0.06)
    r2 = env.create_rating(1400, 30)
    r3 = env.create_rating(1550, 100)
    r4 = env.create_rating(1700, 300)

    assert assess_value(env.expect_score(r1, r2), 0.639)
    assert assess_value(env.expect_score(r1, r3), 0.432)
    assert assess_value(env.expect_score(r1, r4), 0.303)

    rated: Rating = env.rate(r1, [(WIN, r2), (LOSS, r3), (LOSS, r4)])
    assert assess_value(rated.r, 1464.051)
    assert assess_value(rated.RD, 151.516)
    assert assess_value(rated.sigma, 0.05999)


def test_glicko2_np() -> None:
    """
    This test executes example I made.
    """
    env: Glicko2_np = Glicko2_np(tau=1.1)
    r1 = env.create_rating(1200, 40, 0.08)
    r2 = env.create_rating(1700, 100)
    r3 = env.create_rating(1600, 50)
    r4 = env.create_rating(1800, 200)
    assert assess_value(env.expect_score(r1, r2), 0.06046)
    assert assess_value(env.expect_score(r1, r3), 0.09328)
    assert assess_value(env.expect_score(r1, r4), 0.05136)

    r1_new: Rating = env.rate(
        r1, [(WIN, r2), (WIN, r2), (WIN, r3), (WIN, r4), (LOSS, r4)]
    )
    assert assess_value(r1_new.r, 1235.193)
    assert assess_value(r1_new.RD, 42.132)
    assert assess_value(r1_new.sigma, 0.082)
