"""
These functions handle talking to the database and should be considered
impure.
"""

from ..config import config

from ..models import (
    UltimateOXGame,
    UltimateOXMove,
    UltimateOXProfile,
)

from sqlalchemy import or_, and_
from sqlalchemy import func
import datetime

from . import (
    rules,
    actions
)

def get_profile(user_id):
    the_profile = config['DBSession'].query(UltimateOXProfile).filter(UltimateOXProfile.user == user_id).first()
    
    if the_profile is None:
        the_profile = add_empty_profile(user_id)
    
    return the_profile

def add_empty_profile(user_id):
    the_profile = UltimateOXProfile()
    the_profile.user = user_id
    
    config['DBSession'].add(the_profile)
    return the_profile

def get_game_list(user_id):
    "Games waiting for us to make our move"
    User = config['User']
    
    filters = (
        or_(
            and_(UltimateOXGame.player1 == user_id, "mod(ultimate_ox_games.turn, 2) = 0", User.id == UltimateOXGame.player2),
            and_(UltimateOXGame.player2 == user_id, "mod(ultimate_ox_games.turn, 2) = 1", User.id == UltimateOXGame.player1),
        ),
        UltimateOXGame.winner == None,
    )
    
    return config['DBSession'].query(UltimateOXGame.id, User.name, UltimateOXGame.turn).filter(*filters)

def get_waiting_game_list(user_id):
    "Games waiting for our opponent to make a move"
    User = config['User']
    
    filters = (
        or_(
            and_(UltimateOXGame.player1 == user_id, "mod(ultimate_ox_games.turn, 2) = 1", User.id == UltimateOXGame.player2),
            and_(UltimateOXGame.player2 == user_id, "mod(ultimate_ox_games.turn, 2) = 0", User.id == UltimateOXGame.player1),
        ),
        UltimateOXGame.winner == None,
    )
    
    return config['DBSession'].query(UltimateOXGame.id, User.name, UltimateOXGame.turn).filter(*filters)

def get_recent_game_list(user_id, limit=5):
    "The most recently completed games, we return the id of the winner as a 4th attribute"
    User = config['User']
    
    filters = (
        or_(
            and_(UltimateOXGame.player1 == user_id, User.id == UltimateOXGame.player2),
            and_(UltimateOXGame.player2 == user_id, User.id == UltimateOXGame.player1),
        ),
        UltimateOXGame.winner != None,
    )
    
    return config['DBSession'].query(
        UltimateOXGame.id, User.name, UltimateOXGame.turn, UltimateOXGame.winner
    ).filter(*filters).order_by(UltimateOXGame.id.desc()).limit(limit)

def find_user(identifier):
    User = config['User']
    
    if type(identifier) == str:
        found = config['DBSession'].query(User.id).filter(User.name == identifier).first()
        if found == None:
            return None
        return config['get_user']({'id':found[0], 'name':identifier})
    
    elif type(identifier) == int:
        found = config['DBSession'].query(User.name).filter(User.id == identifier).first()
        if found == None:
            return None
        return config['get_user']({'id':identifier, 'name':found[0]})
    
    else:
        raise KeyError("No handler for identifier type of '{}'".format(type(identifier)))

def new_game(p1, p2, rematch=None):
    game               = UltimateOXGame()
    game.player1       = p1.id
    game.player2       = p2.id
    game.started       = datetime.datetime.now()
    game.turn          = 0
    game.source        = rematch
    
    game.overall_state = str(rules.empty_overall)
    game.current_state = str(rules.empty_board)
    game.active_board  = -1
    
    config['DBSession'].add(game)
    
    # Get game ID
    game_id = config['DBSession'].query(UltimateOXGame.id).filter(
        UltimateOXGame.player1 == p1.id,
        UltimateOXGame.player2 == p2.id,
    ).order_by(UltimateOXGame.id.desc()).first()[0]
    
    return game_id

def get_game(game_id):
    the_game = config['DBSession'].query(UltimateOXGame).filter(UltimateOXGame.id == game_id).first()
    
    if the_game == None:
        raise ValueError("We were unable to find the game")
    
    return the_game

def add_turn(the_game, square):
    new_turn           = UltimateOXMove()
    new_turn.game      = the_game.id
    new_turn.player    = rules.current_player(the_game)
    
    new_turn.move      = square
    new_turn.timestamp = datetime.datetime.now()
    
    config['DBSession'].add(new_turn)

def end_game(the_game):
    the_game.complete = True
    
    current_player = rules.current_player_number(the_game.turn)
    the_game.winner = rules.get_player_user_id(the_game, 3-current_player)
    the_game.active_board = -1
    
def draw_game(the_game):
    the_game.complete = True
    the_game.winner = -1

def perform_move(the_game, square):
    add_turn(the_game, square)
    actions.perform_move(the_game, square)
    the_game.turn += 1
    
    actions.set_active_board(the_game, square)
    
    rules.check_for_sub_win(the_game, square)
    
    end_result = rules.test_win(the_game.overall_state)
    if end_result in ("1", "2"):
        end_game(the_game)
    elif " " not in the_game.current_state:
        draw_game(the_game)
    
    config['DBSession'].add(the_game)

def completed_games(user_id, opponent_id=None):
    if opponent_id != None:
        filters = (
            or_(
                and_(UltimateOXGame.player1 == user_id, UltimateOXGame.player2 == opponent_id),
                and_(UltimateOXGame.player2 == user_id, UltimateOXGame.player1 == opponent_id),
            ),
            UltimateOXGame.winner != None,
        )
    else:
        filters = (
            or_(UltimateOXGame.player1 == user_id, UltimateOXGame.player2 == user_id),
            UltimateOXGame.winner != None,
        )
    return config['DBSession'].query(func.count(UltimateOXGame.id)).filter(*filters).first()[0]

def games_in_progress(user_id, opponent_id=None):
    if opponent_id != None:
        filters = (
            or_(
                and_(UltimateOXGame.player1 == user_id, UltimateOXGame.player2 == opponent_id),
                and_(UltimateOXGame.player2 == user_id, UltimateOXGame.player1 == opponent_id),
            ),
            UltimateOXGame.winner == None,
        )
    else:
        filters = (
            or_(UltimateOXGame.player1 == user_id, UltimateOXGame.player2 == user_id),
            UltimateOXGame.winner == None,
        )
    return config['DBSession'].query(func.count(UltimateOXGame.id)).filter(*filters).first()[0]
    
def games_won(user_id, opponent_id=None):
    filters = [
        UltimateOXGame.winner == user_id,
    ]
    if opponent_id != None:
        filters.append(or_(
            UltimateOXGame.player1 == opponent_id,
            UltimateOXGame.player2 == opponent_id
        ))
    
    return config['DBSession'].query(func.count(UltimateOXGame.id)).filter(*filters).first()[0]

def games_lost(user_id, opponent_id=None):
    if opponent_id != None:
        filters = (
            UltimateOXGame.winner == opponent_id,
            or_(
                UltimateOXGame.player1 == user_id,
                UltimateOXGame.player2 == user_id
            ))
    else:
        filters = (
            or_(UltimateOXGame.player1 == user_id, UltimateOXGame.player2 == user_id),
            UltimateOXGame.winner != user_id,
            UltimateOXGame.winner != None,
        )
    return config['DBSession'].query(func.count(UltimateOXGame.id)).filter(*filters).first()[0]

def games_drawn(user_id, opponent_id=None):
    if opponent_id != None:
        filters = (
            or_(
                and_(UltimateOXGame.player1 == user_id, UltimateOXGame.player2 == opponent_id),
                and_(UltimateOXGame.player2 == user_id, UltimateOXGame.player1 == opponent_id),
            ),
            UltimateOXGame.winner == -1,
        )
    else:
        
        filters = (
            or_(UltimateOXGame.player1 == user_id, UltimateOXGame.player2 == user_id),
            UltimateOXGame.winner == -1,
        )
    return config['DBSession'].query(func.count(UltimateOXGame.id)).filter(*filters).first()[0]

def get_stats(user_id, opponent_id=None):
    stats = dict(
        completed_games   = completed_games(user_id, opponent_id),
        games_in_progress = games_in_progress(user_id, opponent_id),
        
        games_won   = games_won(user_id, opponent_id),
        games_lost  = games_lost(user_id, opponent_id),
        games_drawn = games_drawn(user_id, opponent_id),
    )
    
    stats['win_ratio'] = rules.win_ratio(stats['games_won'], stats['completed_games'])
    
    return stats
