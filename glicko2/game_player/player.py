from datetime import date
from typing import Any

from .rating import Rating


class Player:
    """
    A player has unique_id, rating, and rating history.
    unique_id must be unique.
    """

    unique_id: int
    rating: Rating
    rating_history: list[tuple[date, Rating]]

    def __init__(
        self,
        unique_id: int,
        rating: Rating | None = None,
        rating_history: list[tuple[date, Rating]] | None = None,
    ):
        """
        arguments:
            unique_id : it is required. It must be unique number and corresponds to one player.
            rating : optional. When it lacks, inital rating would be used.
            rating_history : optional.
        """
        self.unique_id = unique_id
        if rating is None:
            self.rating = Rating()
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

    def to_dict(self) -> dict[str, Any]:
        """
        convert date to isoformat for json dump
        """
        rating_history_for_dict: list[Any] = []
        for rating_date, rating_in_history in self.rating_history:
            rating_history_for_dict.append({rating_date.isoformat(): rating_in_history.to_dict()})
        return {"unique_id": self.unique_id, "rating": self.rating.to_dict(), "rating_history": rating_history_for_dict}
