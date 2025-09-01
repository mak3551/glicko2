from .constant_value import R_INITIAL, RD_INITIAL, SIGMA_INITIAL


class Rating:
    """
    Rating in old Glicko (and Elo) scale.
    Each player has a rating, a rating deviation, and a rating volatility.
    In this code, a rating is "r", a rating deviation is "rd", and a rating volatility is "sigma".
    In the Mark Glickman's paper, "r", "RD", and "σ". https://www.glicko.net/glicko/glicko2.pdf
    """

    r: float
    rd: float
    sigma: float

    def __init__(self, r: float = R_INITIAL, rd: float = RD_INITIAL, sigma: float = SIGMA_INITIAL):
        self.r = r
        self.rd = rd
        self.sigma = sigma

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(r={self.r}, rd={self.rd}, sigma={self.sigma})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rating):
            return NotImplemented
        return self.r == other.r and self.rd == other.rd and self.sigma == other.sigma

    def _flatter(self) -> list[float]:
        """
        convert this object to list.
        """
        return [self.r, self.rd, self.sigma]


class RatingInGlicko2:
    """
    Rating in Glicko-2 scale.
    """

    mu: float
    phi: float
    sigma: float

    def __init__(self, mu: float, phi: float, sigma: float):
        self.mu = mu
        self.phi = phi
        self.sigma = sigma

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(mu={self.mu}, phi={self.phi}, sigma={self.sigma})"
