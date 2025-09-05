from dataclasses import dataclass
from datetime import date

from .player import Player


@dataclass(slots=True)
class GamePlayer:
    name: str
    player: Player
    first_mach_date: date


class GamePlayerList:
    list_game_player: list[GamePlayer]
    next_unique_id: int
    name_set: set[str]
    name_player_dict: dict[str, GamePlayer]  # value is GamePlayer object, key is its name.
    uniqueid_player_dict: dict[int, GamePlayer]  # value is GamePlayer object, key is unique_id.

    def __init__(self) -> None:
        self.list_game_player = []
        self.next_unique_id = 1
        self.name_set = set()
        self.name_player_dict = {}
        self.uniqueid_player_dict = {}

    def add_game_player(self, name: str, mach_date: date) -> None:
        """
        make GamePlayer object and add it in list_game_player.

        if a name is already registered, skipped.
        When added, name_set, name_player_dict and uniqueid_player_dict are automatically updated.
        """
        if name in self.name_set:
            return None
        new_game_player: GamePlayer = GamePlayer(name, Player(self.next_unique_id), mach_date)
        self.list_game_player.append(new_game_player)
        self.name_set.add(name)
        assert name not in self.name_player_dict
        self.name_player_dict[name] = new_game_player
        self.uniqueid_player_dict[self.next_unique_id] = new_game_player
        self.next_unique_id += 1
        return None
