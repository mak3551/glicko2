from dataclasses import dataclass

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


@dataclass(slots=True, frozen=True)
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

    def to_dict(self) -> dict[str, float]:
        return {"r": self.r, "rd": self.rd, "sigma": self.sigma}


def _scale_to_glicko2(rating: Rating) -> RatingInGlicko2:
    """
    In the Mark Glickman's paper, he says the rating scale for Glicko-2 is different from that of Original Glicko (and Elo).
    This function converts rating and RD from old-style to Glicko-2's scale (Step 2 in the paper).
    """
    mu: float = (rating.r - REF_R) / RATIO
    phi: float = rating.rd / RATIO
    return RatingInGlicko2(mu, phi, rating.sigma)


def _scale_to_oldstyle(rating_in_glicko2: RatingInGlicko2) -> Rating:
    """
    This function converts rating and RD from Glicko-2 to old-style.
    """
    r: float = rating_in_glicko2.mu * RATIO + REF_R
    rd: float = rating_in_glicko2.phi * RATIO
    return Rating(r, rd, rating_in_glicko2.sigma)
