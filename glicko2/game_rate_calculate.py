from datetime import date, timedelta

from .game_player.game_player import GamePlayerList
from .game_player.player import Player
from .rate_period import rate_period
from .rating_system.glicko2.glicko2 import Glicko2
from .rating_system.rating_system import RatingSystem


def _extract_player_list_from_gamelist(
    gamelist: list[tuple[str | date, str, str, float]],
) -> tuple[list[tuple[str | date, str, str, float]], GamePlayerList]:
    """
    sort gamelist and extract information of players from it.

    argument is a list like this:
        [(date, name_1, name_2, result), (date, name_1, name_2, result), ...]
    date could be str or date. If str, it must be ISO style like "2000-04-01"
    If date is invalid str, it raises ValueError.
    all date must be same type. If not, it raises TypeError.
    name_1 and name_2 must not be same. If so, it raises ValueError.
    result is float. if name_1 wins, result is 1.0. If name_1 loses, result is 0.0.
    If draw, result is 0.5.

    It returns a sorted gamelist and a list of players extracted from it.
    """
    # sorted() raises TypeError if first element of gamelist is not same
    # i.e. [('2020-1-1','a','b',1.0),(date(2020, 3, 4),'c','d',0.0),...] raises TypeError
    sorted_gamelist: list[tuple[str | date, str, str, float]] = sorted(gamelist, key=lambda x: x[0])
    playerlist: GamePlayerList = GamePlayerList()
    for game in sorted_gamelist:
        # date.isofromformat() raises ValueError if game[0] is invalid format string.
        match_date: date = game[0] if isinstance(game[0], date) else date.fromisoformat(game[0])
        if game[1] == game[2]:
            raise ValueError
        playerlist.add_game_player(game[1], match_date)
        playerlist.add_game_player(game[2], match_date)

    return sorted_gamelist, playerlist


def _divide_sorted_gamelist(
    sorted_gamelist: list[tuple[date | str, str, str, float]], player_list: GamePlayerList, days: timedelta | int
) -> list[tuple[list[tuple[int, int, float]], date]]:
    """
    divide gamelist per days.

    arguments:
        sorted_gamelist: it must be sorted by date.
        player_list: GamePlayerList
        days: gamelist would be divided per days. timedelta or int.
    """
    per_days: timedelta = days if isinstance(days, timedelta) else timedelta(days=days)
    divided_gamelist: list[tuple[list[tuple[int, int, float]], date]] = []
    temp_start_date: date | None = None
    temp_game_list: list[tuple[int, int, float]] = []

    for game in sorted_gamelist:
        game_date: date = game[0] if isinstance(game[0], date) else date.fromisoformat(game[0])
        game_player1_name: str = game[1]
        game_player2_name: str = game[2]
        game_result: float = game[3]
        # set date when first loop
        if temp_start_date is None:
            temp_start_date = game_date
        # if exceeds per_days, append current list, and creates new list, and update temp_start_date
        if game_date - temp_start_date > per_days:
            divided_gamelist.append((temp_game_list, game_date))
            temp_game_list = []
            temp_start_date = game_date
        temp_game_list.append(
            (
                player_list.name_player_dict[game_player1_name].player.unique_id,
                player_list.name_player_dict[game_player2_name].player.unique_id,
                game_result,
            )
        )

    return divided_gamelist


def calculate_rating_in_rate_period(
    sorted_gamelist_in_rate_period: list[tuple[int, int, float]], player_list: GamePlayerList, system: RatingSystem, rating_date: date
) -> None:
    """
    rating_date is start date of **next** rating period.
    player_list is updated internally
    """
    list_gameplayer = player_list.list_game_player
    player_list_before_rate_period: list[Player] = []
    # player_list_before_rate_period is list of players whose first matche is before rating_date
    for gameplayer in list_gameplayer:
        if gameplayer.first_mach_date < rating_date:
            player_list_before_rate_period.append(gameplayer.player)
    matchlist_rate_period: list[tuple[Player, Player, float]] = []
    # convert matches from tuple[int,int,float] to list[Player,Player,float]
    for g in sorted_gamelist_in_rate_period:
        g_player1_id: int = g[0]
        g_player2_id: int = g[1]
        matchlist_rate_period.append(
            (player_list.uniqueid_player_dict[g_player1_id].player, player_list.uniqueid_player_dict[g_player2_id].player, g[2])
        )
    updated_player_list: list[Player] = rate_period(matchlist_rate_period, player_list_before_rate_period, system, rating_date)
    for updated_player in updated_player_list:
        id_updated_player: int = updated_player.unique_id
        player_list.uniqueid_player_dict[id_updated_player].player = updated_player
    return None


def game_rate_calculate(
    gamelist: list[tuple[str | date, str, str, float]], per_days: int | timedelta = 90, rating_system: RatingSystem | None = None
) -> GamePlayerList:
    """
        argument is a list like this:
        [(date, name_1, name_2, result), (date, name_1, name_2, result), ...]
    date could be str or date. If str, it must be ISO style like "2000-04-01"
    name_1 and name_2 must not be same.
    result is float. if name_1 wins, result is 1.0. If name_1 loses, result is 0.0.
    If draw, result is 0.5.
    """
    if rating_system is None:
        rating_system = Glicko2()
    sorted_gamelist, player_list = _extract_player_list_from_gamelist(gamelist)
    divided_gamelist = _divide_sorted_gamelist(sorted_gamelist, player_list, per_days)
    for game_rate_period in divided_gamelist:
        gamelist_in_period: list[tuple[int, int, float]] = game_rate_period[0]
        rating_date: date = game_rate_period[1]
        calculate_rating_in_rate_period(gamelist_in_period, player_list, rating_system, rating_date)
    return player_list
