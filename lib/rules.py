import math

empty_overall = " " * 9
empty_board   = " " * 81

boards = 9
height = 3
width  = 3

wins = (
    # Horrizontal
    (0,1,2),
    (3,4,5),
    (6,7,8),
    
    # Vertical
    (0,3,6),
    (1,4,7),
    (2,5,8),
    
    # Diagonal
    (0,4,8),
    (6,4,2),
)

def get_player_user_id(the_game, player_number):
    if player_number == 1: return the_game.player1
    if player_number == 2: return the_game.player2
    raise KeyError("There is no player of {}".format(player_number))

def get_player_game_number(the_game, player_id):
    if the_game.player1 == player_id: return 1
    if the_game.player2 == player_id: return 2
    raise KeyError("None of the players have an ID of {}".format(player_id))

def current_player(the_game):
    return get_player_user_id(the_game, current_player_number(the_game.turn))

def current_player_number(game_turn):
    if game_turn % 2 == 0: return 1
    else: return 2

def sub_board(total_board, board_number):
    start = board_number * 9
    stop  = start + 9
    return total_board[start:stop]

def square_to_boardsquare(square):
    board = math.floor(square / 9)
    bsquare = square % 9
    return board, bsquare

def player_boards(boards, player):
    for i, b in enumerate(boards):
        if b == str(player):
            yield i

def player_squares(squares, player):
    for i, s in enumerate(squares):
        if s == str(player):
            yield i

def is_move_valid(active_board, current_state, square):
    b, s = square_to_boardsquare(square)
    
    if current_state[square] != " ": return False
    if active_board not in (-1, b): return False
    return True

def test_win(board):
    for w1, w2, w3 in wins:
        if board[w1] != " ":
            if board[w1] == board[w2] == board[w3]:
                return board[w1]
    return False

def check_for_sub_win(the_game, square):
    b, s = square_to_boardsquare(square)
    
    if the_game.overall_state[b] == " ":
        partial = sub_board(the_game.current_state, b)
        result = test_win(partial)
        
        if result != False:
            mutable_board = list(the_game.overall_state)
            mutable_board[b] = str(result)
            the_game.overall_state = "".join(mutable_board)

def win_ratio(wins, total_games, decimal_points=2):
    if total_games == 0: return 0
    if wins == 0: return 0
    return round(100 * (wins / total_games), decimal_points)
