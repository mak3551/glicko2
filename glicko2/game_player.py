from dataclasses import dataclass
from datetime import date

from glicko2 import Player


@dataclass(slots=True)
class GamePlayer:
    name: str
    player: Player
    first_mach_date: date


class GamePlayerList:
    list_game_player: list[GamePlayer]
    next_unique_id: int

    def __init__(self) -> None:
        self.list_game_player = []
        self.next_unique_id = 1

    def get_name_list(self) -> list[str]:
        """
        This returns a list of all known players.
        """
        return [p.name for p in self.list_game_player]

    def get_uniqueid_name_dict(self) -> dict[int, str]:
        """
        This returns a dict. Keys are unique_id, values are names of player.
        """
        return {p.player.unique_id: p.name for p in self.list_game_player}

    def get_name_player_dict(self) -> dict[str, Player]:
        """
        This returns a dict. Keys are name, values are Player object.
        """
        return {p.name: p.player for p in self.list_game_player}


# def glicko2_calculate( gamelist : list[tuple[str | date, str, str, float]]):
#     """
#     [(date, name_1, name_2, result)]
#     data could be str or date. If str, it must be ISO style like "2000-4-1"
#     """
#     sorted_gamelist : list[tuple[str | date, str, str, float]] = sorted(gamelist, key=lambda x: x[0])
#     return sorted_gamelist
