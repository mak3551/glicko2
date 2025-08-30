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
    name_set: set[str]
    name_player_dict: dict[str, GamePlayer]  # value is GamePlayer object, key is its name.
    uniqueid_name_dict: dict[int, GamePlayer]  # value is GamePlayer object, key is unique_id.

    def __init__(self) -> None:
        self.list_game_player = []
        self.next_unique_id = 1
        self.name_set = set()
        self.name_player_dict = {}
        self.uniqueid_name_dict = {}

    def add_game_player(self, name: str, mach_date: date) -> None:
        """
        make GamePlayer object and add it in list_game_player.

        if a name is already registered, skipped.
        When added, name_set, name_player_dict and uniqueid_name_dict are automatically updated.
        """
        if name in self.name_set:
            return None
        new_game_player: GamePlayer = GamePlayer(name, Player(self.next_unique_id), mach_date)
        self.list_game_player.append(new_game_player)
        self.name_set.add(name)
        assert name not in self.name_player_dict
        self.name_player_dict[name] = new_game_player
        self.uniqueid_name_dict[self.next_unique_id] = new_game_player
        self.next_unique_id += 1
        return None


def extract_player_list_from_gamelist(
    gamelist: list[tuple[str | date, str, str, float]],
) -> tuple[list[tuple[str | date, str, str, float]], GamePlayerList]:
    """
    sort gamelist and extract information of players from it.

    argument is a list like this:
        [(date, name_1, name_2, result), (date, name_1, name_2, result), ...]
    date could be str or date. If str, it must be ISO style like "2000-04-01"
    name_1 and name_2 must not be same.
    result is float. if name_1 wins, result is 1.0. If name_1 loses, result is 0.0.
    If draw, result is 0.5.

    It returns a sorted gamelist and a list of players extracted from it.
    """
    sorted_gamelist: list[tuple[str | date, str, str, float]] = sorted(gamelist, key=lambda x: x[0])
    playerlist: GamePlayerList = GamePlayerList()
    for game in sorted_gamelist:
        match_date: date = game[0] if isinstance(game[0], date) else date.fromisoformat(game[0])
        if game[1] == game[2]:
            raise RuntimeError
        playerlist.add_game_player(game[1], match_date)
        playerlist.add_game_player(game[2], match_date)

    return sorted_gamelist, playerlist
