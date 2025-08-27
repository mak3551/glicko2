# -*- coding: utf-8 -*-
from src.glicko2 import Glicko2, WIN, LOSS, Rating
import math


class almost():
    val : Rating
    precision : int

    def __init__(self, val : Rating, precision : int=3):
        self.val = val
        self.precision = precision

    def almost_equals(self, val1 : float, val2 : float) -> bool:
        if round(val1, self.precision) == round(val2, self.precision):
            return True
        fmt : str = "%.{0}f".format(self.precision)
        def mantissa(f : float, fmt : str) -> int:
            return int((fmt % f).replace(".", ""))
        return int(math.fabs(mantissa(val1, fmt) - mantissa(val2, fmt))) <= 1

    def almost_equals_rating(self, other : Rating) -> bool:
        return self.almost_equals(self.val.mu, other.mu) and self.almost_equals(
            self.val.sigma, other.sigma
        )

    def __repr__(self) -> str:
        return repr(self.val)


def test_glickman_example() -> None:
    env : Glicko2 = Glicko2(tau=0.5)
    r1 = env.create_rating(1500, 200, 0.06)
    r2 = env.create_rating(1400, 30)
    r3 = env.create_rating(1550, 100)
    r4 = env.create_rating(1700, 300)
    rated : Rating = env.rate(r1, [(WIN, r2), (LOSS, r3), (LOSS, r4)])
    # env.create_rating2(1464.06, 151.52, 0.05999)
    assert almost(rated).almost_equals_rating( env.create_rating(1464.051, 151.515, 0.05999) )
