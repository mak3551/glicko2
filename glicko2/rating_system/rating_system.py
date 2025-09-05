from abc import ABC, abstractmethod

from ..game_player.rating import Rating


class RatingSystem(ABC):
    @abstractmethod
    def rate(self, rating: Rating, series: list[tuple[float, Rating]]) -> Rating:
        pass
