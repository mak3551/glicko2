from glicko2 import glicko2


class Player:
    """
    A player has id and rating.
    id must be unique.
    """

    id: int
    rating: glicko2.Rating

    def __init__(self, id: int, rating: glicko2.Rating):
        self.id = id
        self.rating = rating
