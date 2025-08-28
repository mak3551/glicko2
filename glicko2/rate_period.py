from glicko2.player import Player
from glicko2.glicko2 import Rating


def rate_period(
    matches: list[tuple[Player, Player, float]], players_list: list[Player]
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
    """

    # not implemented
    return []


def _get_series_of_player(
    matches: list[tuple[Player, Player, float]], player: Player
) -> list[tuple[float, Rating]]:
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
        elif player_foemer != player and player_latter != player:
            continue
        elif player_foemer == player:
            series.append((result, player_latter.rating))
        elif player_latter == player:
            series.append((1.0 - result, player_foemer.rating))
        else:
            raise RuntimeError("Unexpected error occurred.")
    return series
