"""
glicko2
~~~~~~~

The Glicko2 rating system.
This code is a fork of https://github.com/sublee/glicko2.

:copyright: (c) 2025, by mak3551
:copyright: (c) 2012 by Heungsub Lee
:license: BSD, see LICENSE for more details.
"""

import math

import numpy as np
import numpy.typing as npt

from ..constant_value import DRAW, EPSILON, LOSS, RD_INITIAL, SIGMA_INITIAL, TAU, WIN
from ..rating import Rating, RatingInGlicko2


class Glicko2Np:
    tau: float

    def __init__(self, tau: float = TAU):
        self.tau = tau

    def create_rating(self, r: float, rd: float = RD_INITIAL, sigma: float = SIGMA_INITIAL) -> Rating:
        return Rating(r, rd, sigma)

    def scale_down(self, rating: Rating, ratio: float = 173.7178, ref_r: float = 1500) -> RatingInGlicko2:
        """
        In the Mark Glickman's paper, he says the rating scale for Glicko-2 is different from that of Original Glicko (and Elo).
        This function converts rating and RD from old-style to Glicko-2's scale (Step 2 in the paper).
        """
        mu: float = (rating.r - ref_r) / ratio
        phi: float = rating.rd / ratio
        return RatingInGlicko2(mu, phi, rating.sigma)

    def _scale_down_ndarray(
        self,
        series_ndarray: npt.NDArray[np.float64],
        ratio: float = 173.7178,
        ref_r: float = 1500,
    ) -> None:
        """
        destractive function.
        This function converts series_ndarray from traditional scale to Glicko2's scale.
        """
        series_ndarray[:, 1] = (series_ndarray[:, 1] - ref_r) / ratio
        series_ndarray[:, 2] = series_ndarray[:, 2] / ratio

    def scale_up(self, rating: RatingInGlicko2, ratio: float = 173.7178, ref_r: float = 1500) -> Rating:
        """
        This function converts rating and RD from Glicko-2 to old-style.
        """
        r: float = rating.mu * ratio + ref_r
        rd: float = rating.phi * ratio
        return Rating(r, rd, rating.sigma)

    def reduce_impact(self, rating: RatingInGlicko2) -> float:
        """
        g(φ)
        This function reduces the impact of
        games as a function of an opponent's RD.
        """
        return 1.0 / math.sqrt(1 + (3 * rating.phi**2) / (math.pi**2))

    def _reduce_impact_ndarray(self, phi_ndarray: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        return 1.0 / np.sqrt(1.0 + (3.0 * (phi_ndarray**2)) / (np.pi**2))

    def expect_score_in_glicko2(self, rating: RatingInGlicko2, other_rating: RatingInGlicko2, impact: float) -> float:
        """
        E(μ,μj,φj)
        It calculates expected outcome of a game.
        """
        return 1.0 / (1 + math.exp(-impact * (rating.mu - other_rating.mu)))

    def _expect_score_in_glicko2_ndarray(
        self,
        mu: float,
        mu_opponents_ndarray: npt.NDArray[np.float64],
        impact_ndarray: npt.NDArray[np.float64],
    ) -> npt.NDArray[np.float64]:
        return 1.0 / (1 + np.exp((-1.0) * impact_ndarray * (mu - mu_opponents_ndarray)))

    def determine_sigma(self, rating: RatingInGlicko2, difference: float, variance: float) -> float:
        """Determines new sigma. (Step 5)"""
        phi: float = rating.phi
        difference_squared: float = difference**2
        # 1. Let a = ln(s^2), and define f(x)
        alpha: float = math.log(rating.sigma**2)

        def f(x: float) -> float:
            """This function is twice the conditional log-posterior density of
            phi, and is the optimality criterion.
            """
            tmp: float = phi**2 + variance + math.exp(x)
            a: float = math.exp(x) * (difference_squared - tmp) / (2 * tmp**2)
            b: float = (x - alpha) / (self.tau**2)
            return a - b

        # 2. Set the initial values of the iterative algorithm.
        a: float = alpha
        b: float = 0.0
        if difference_squared > phi**2 + variance:
            b = math.log(difference_squared - phi**2 - variance)
        else:
            k = 1
            while f(alpha - k * math.sqrt(self.tau**2)) < 0:
                k += 1
            b = alpha - k * math.sqrt(self.tau**2)
        # 3. Let fA = f(A) and f(B) = f(B)
        f_a, f_b = f(a), f(b)
        # 4. While |B-A| > e, carry out the following steps.
        # (a) Let C = A + (A - B)fA / (fB-fA), and let fC = f(C).
        # (b) If fCfB < 0, then set A <- B and fA <- fB; otherwise, just set
        #     fA <- fA/2.
        # (c) Set B <- C and fB <- fC.
        # (d) Stop if |B-A| <= e. Repeat the above three steps otherwise.
        while abs(b - a) > EPSILON:
            c: float = a + (a - b) * f_a / (f_b - f_a)
            f_c: float = f(c)
            if f_c * f_b < 0:
                a, f_a = b, f_b
            else:
                f_a /= 2
            b, f_b = c, f_c
        # 5. Once |B-A| <= e, set s' <- e^(A/2)
        result_sigma: float = math.exp(1) ** (a / 2)
        return result_sigma

    def _convert_series_to_ndarray(self, series: list[tuple[float, Rating]]) -> npt.NDArray[np.float64]:
        return np.array([[t[0], t[1].r, t[1].rd, t[1].sigma] for t in series])

    def rate(self, rating: Rating, series: list[tuple[float, Rating]]) -> Rating:
        """
        It returns new rating from old rating and game outcomes.
            rating : old rating
            series : game outcomes in rating period, like [( WIN , player1 ), ( LOSE, player2), ( LOSE , player3)]

        In the Mark Glickman's paper, he says Glicko-2 works best when the number of games in a rating period is moderate to large,
        say an average of at least 10-15 games per player in a rating period.
        """
        series_ndarray = self._convert_series_to_ndarray(series)
        # Step 2. For each player, convert the rating and RD's onto the
        #         Glicko-2 scale.
        rating_in_glicko2: RatingInGlicko2 = self.scale_down(rating)
        if not series:
            # If the team didn't play in the series, do only Step 6
            phi_star: float = math.sqrt(rating_in_glicko2.phi**2 + rating_in_glicko2.sigma**2)
            return self.scale_up(RatingInGlicko2(rating_in_glicko2.mu, phi_star, rating.sigma))
        series_ndarray = self._convert_series_to_ndarray(series)
        self._scale_down_ndarray(series_ndarray)
        # Step 3. Compute the quantity v. This is the estimated variance of the
        #         team's/player's rating based only on game outcomes.
        # Step 4. Compute the quantity difference, the estimated improvement in
        #         rating by comparing the pre-period rating to the performance
        #         rating based only on game outcomes.

        # "impact_ndarray" is g(φ).
        impact_ndarray: npt.NDArray[np.float64] = self._reduce_impact_ndarray(series_ndarray[:, 2])
        # "expected_score_ndarray" is E(μ, μj, φj).
        expect_score_ndarray: npt.NDArray[np.float64] = self._expect_score_in_glicko2_ndarray(
            rating_in_glicko2.mu,
            series_ndarray[:, 1],
            impact_ndarray,
        )
        # The value of "variance" is the quantity v (Step 3).
        variance: np.float64 = 1.0 / np.sum((impact_ndarray**2) * expect_score_ndarray * (1 - expect_score_ndarray))
        # The value of "difference" is the quantity ∆ (Step 4).
        difference: np.float64 = variance * np.sum(impact_ndarray * (series_ndarray[:, 0] - expect_score_ndarray))

        # Step 5. Determine the new value, Sigma', ot the sigma. This
        #         computation requires iteration.
        sigma: float = self.determine_sigma(rating_in_glicko2, difference, variance)
        # Step 6. Update the rating deviation to the new pre-rating period
        #         value, Phi*.
        phi_star = math.sqrt(rating_in_glicko2.phi**2 + sigma**2)
        # Step 7. Update the rating and RD to the new values, Mu' and Phi'.
        phi: float = 1.0 / math.sqrt(1 / phi_star**2 + 1 / variance)
        mu: float = rating_in_glicko2.mu + phi**2 * (difference / variance)
        # Step 8. Convert ratings and RD's back to original scale.
        return self.scale_up(RatingInGlicko2(mu, phi, sigma))

    def rate_1vs1(self, rating1: Rating, rating2: Rating, drawn: bool = False) -> tuple[Rating, Rating]:
        return (
            self.rate(rating1, [(DRAW if drawn else WIN, rating2)]),
            self.rate(rating2, [(DRAW if drawn else LOSS, rating1)]),
        )

    def quality_1vs1(self, rating1: RatingInGlicko2, rating2: RatingInGlicko2) -> float:
        expected_score1 = self.expect_score_in_glicko2(rating1, rating2, self.reduce_impact(rating1))
        expected_score2 = self.expect_score_in_glicko2(rating2, rating1, self.reduce_impact(rating2))
        expected_score = (expected_score1 + expected_score2) / 2
        return 2 * (0.5 - abs(0.5 - expected_score))

    def expect_score(self, rating1: Rating, rating2: Rating) -> float:
        """
        calculates probablity (rating1 win).
        """
        rating1_glicko2: RatingInGlicko2 = self.scale_down(rating1)
        rating2_glicko2: RatingInGlicko2 = self.scale_down(rating2)
        impact: float = self.reduce_impact(rating2_glicko2)
        expectation: float = self.expect_score_in_glicko2(rating1_glicko2, rating2_glicko2, impact)
        return expectation
