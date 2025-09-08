from collections.abc import Iterable
from datetime import date

from .game_player.player import Player
from .game_player.rating import Rating
from .rating_system.glicko2.glicko2 import Glicko2
from .rating_system.rating_system import RatingSystem


def rate_period(
    matches: Iterable[tuple[Player, Player, float]],
    players_list: list[Player],
    system: RatingSystem | None = None,
    match_date: date | None = None,
) -> list[Player]:
    """
    calculates rates of each player in a rating period.
    It is preferable in a rating period per player plays at least 10-15 games on average.
    arguments:
        matches : game outcomes. i.e. [ ( player1, player2, 1), ( player3, player4, 0), (player5, player6, 1) ]
            result is from former player's point of view. 1 is WIN, 0 is LOSS. 0.5 is DRAW.
            For example, if player1 wins against player2, (player1, player2, 1)
            If one player's matches against same player, like (player1, player1, 1) exist, error occurred.
        players_list : list of players.
        system : optional. Glicko2 object. If it doesn't set, internaly generated (tau is default).
        match_date : optional. If it is set, rating_history of each player is updated.
    """
    new_players_list: list[Player] = []
    if system is None:
        system = Glicko2()
    for player in players_list:
        series: list[tuple[float, Rating]] = _get_series_of_player(matches, player)
        new_rating: Rating = system.rate(player.rating, series)
        new_rating_history: list[tuple[date, Rating]] = player.rating_history.copy()
        if match_date is not None:
            new_rating_history.append((match_date, new_rating))
        new_player: Player = Player(player.unique_id, new_rating, new_rating_history)
        new_players_list.append(new_player)
    return new_players_list


def _get_series_of_player(matches: Iterable[tuple[Player, Player, float]], player: Player) -> list[tuple[float, Rating]]:
    """
    extract player's game series from matches.
    """
    series: list[tuple[float, Rating]] = []
    for match in matches:
        player_foemer: Player = match[0]
        player_latter: Player = match[1]
        result: float = match[2]
        if player_foemer == player_latter:
            raise RuntimeError("Invalid match detected.")
        elif player not in (player_foemer, player_latter):
            continue
        elif player_foemer == player:
            series.append((result, player_latter.rating))
        elif player_latter == player:
            series.append((1.0 - result, player_foemer.rating))
        else:
            raise RuntimeError("Unexpected error occurred.")
    return series
