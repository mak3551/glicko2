from datetime import date

import glicko2


class Player:
    """
    A player has unique_id, rating, and rating history.
    unique_id must be unique.
    """

    unique_id: int
    rating: glicko2.Rating
    rating_history: list[tuple[date, glicko2.Rating]]

    def __init__(
        self,
        unique_id: int,
        rating: glicko2.Rating | None = None,
        rating_history: list[tuple[date, glicko2.Rating]] | None = None,
    ):
        """
        arguments:
            unique_id : it is required. It must be unique number and corresponds to one player.
            rating : optional. When it lacks, inital rating would be used.
            rating_history : optional.
        """
        self.unique_id = unique_id
        if rating is None:
            self.rating = glicko2.Rating()
        else:
            self.rating = rating
        if rating_history is None:
            self.rating_history = []
        else:
            self.rating_history = rating_history

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return NotImplemented
        return self.unique_id == other.unique_id and self.rating == other.rating

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(unique_id={self.unique_id}, rating={self.rating}, rating_history={self.rating_history})"
