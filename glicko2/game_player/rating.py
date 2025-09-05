from dataclasses import dataclass, field
from functools import lru_cache

from ..constant_value import R_INITIAL, RD_INITIAL, SIGMA_INITIAL

RATIO: float = 173.7178
REF_R: float = 1500


@dataclass(slots=True, frozen=True)
class RatingInGlicko2:
    """
    Rating in Glicko-2 scale.
    """

    mu: float
    phi: float
    sigma: float


@dataclass(slots=True)
class Rating:
    """
    Rating in old Glicko (and Elo) scale.
    Each player has a rating, a rating deviation, and a rating volatility.
    In this code, a rating is "r", a rating deviation is "rd", and a rating volatility is "sigma".
    In the Mark Glickman's paper, "r", "RD", and "σ". https://www.glicko.net/glicko/glicko2.pdf
    """

    r: float = R_INITIAL
    rd: float = RD_INITIAL
    sigma: float = SIGMA_INITIAL
    rating_in_glicko2: RatingInGlicko2 = field(init=False)

    def __post_init__(self) -> None:
        self.rating_in_glicko2 = _scale_to_glicko2(self.r, self.rd, self.sigma)


@lru_cache(maxsize=10000)
def _scale_to_glicko2(r: float, rd: float, sigma: float) -> RatingInGlicko2:
    mu: float = (r - REF_R) / RATIO
    phi: float = rd / RATIO
    return RatingInGlicko2(mu, phi, sigma)
