from glicko2 import glicko2
from datetime import date


class Player:
    """
    A player has id, rating, and rating history.
    id must be unique.
    """

    id: int
    rating: glicko2.Rating
    rating_history: list[tuple[date, glicko2.Rating]]

    def __init__(self, id: int, rating: glicko2.Rating):
        self.id = id
        self.rating = rating
        self.rating_history = []

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.id == other.id and self.rating == other.rating
