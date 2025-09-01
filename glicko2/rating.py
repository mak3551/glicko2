from dataclasses import dataclass

from .constant_value import R_INITIAL, RD_INITIAL, SIGMA_INITIAL


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

    def _flatter(self) -> list[float]:
        """
        convert this object to list.
        """
        return [self.r, self.rd, self.sigma]


@dataclass(slots=True)
class RatingInGlicko2:
    """
    Rating in Glicko-2 scale.
    """

    mu: float
    phi: float
    sigma: float
