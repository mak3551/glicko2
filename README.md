**This Project is under construction. Usage example below doesn't move.**

# glicko2
This project is a fork of https://github.com/sublee/glicko2. 
It is distributed under the BSD 3-Clause License.

This implements Glicko-2 system invented by Mark Glickman. https://www.glicko.net/glicko/glicko2.pdf

## Usage example
    from glicko2 import WIN, LOSS, Player, rate_period
    player_a = Player(id=1)
    player_b = Player(id=2)
    player_c = Player(id=3)
    players_list = [ player_a, player_b, player_c ]

    game_outcomes = [ ( player_a, player_b, WIN ), ( player_a, player_c, WIN), (player_b, player_c, LOSS) ]

    updated_player_list = rate_period( game_outcomes, players_list )
    print( f"player_a rating: {updated_player_list[0].rating.r}" )
    print( f"player_b rating: {updated_player_list[1].rating.r}" )
    print( f"player_c rating: {updated_player_list[2].rating.r}" )
