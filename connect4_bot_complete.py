import numpy as np
import random
import time
import math
import operator
#from numpy.core.multiarray import normalize_axis_index

# Set static variables
ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
BOT = 1

EMPTY = 0
PLAYER_PIECE = 1
BOT_PIECE = 2

WINDOW_LENGTH = 4

# Create a Connect-4 board
def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

# Place a piece on the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check if chosen column has an empty slot
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

# Check which row the piece falls into
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Change orientation of printed board so it looks like Connect-4 on print
def print_board(board):
    print(np.flipud(board))

# Get all locations that could contain a piece
def get_valid_locations(board):
    valid_locations= []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# Look at the board using a 4-piece window to evaluate the whole board & choose a move
def score_position(board, piece):
    score = 0

    # Score centre column
    centre_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    centre_count = centre_array.count(piece)
    score += centre_count * 3

    # Score horizontal positions
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT-3):
            # Create a horizontal window of 4
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score vertical positions
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT-3):
            # Create a vertical window of 4
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive diagonals
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            # Create a positive diagonal window of 4
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative diagonals
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            # Create a negative diagonal window of 4
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# Set window scores based on contents
def evaluate_window(window, piece):
    score = 0
    # Switch scoring based on turn
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = BOT_PIECE

    # Prioritise a winning move
    # Minimax makes this less important
    if window.count(piece) == 4:
        score += 100
    # Make connecting 3 second priority
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    # Make connecting 2 third priority
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2
    # Prioritise blocking an opponent's winning move (but not over bot winning)
    # Minimax makes this less important
    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

# Check to see if the game has been won
def winning_move(board, piece):
    # Check valid horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board [r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check valid vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board [r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check valid positive diagonal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board [r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # check valid negative diagonal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board [r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

# Pick the best move based on the highest-scoring possible move
# Not required if using Minimax
def pick_best_move(board, piece):
    # Retrieve valid locations from function
    valid_locations = get_valid_locations(board)
    # Start with a base-level best score
    best_score = -1000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        # Create a copy of the board to simulate moves
        temp_board = board.copy()
        # Drop a piece in the temporary board and record score
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        # Update piece position based on which returns the highest weighting (score)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

# Define winning moves or no remaining valid locations as terminal nodes (end points)
def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, BOT_PIECE) or len(get_valid_locations(board)) == 0

# Pick the best move by looking at all possible future moves and comparing their scores
def minimax(board, depth, alpha, beta, maximisingPlayer):
    valid_locations = get_valid_locations(board)

    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            # Weight the bot winning really high
            if winning_move(board, BOT_PIECE):
                return (None, 10000000)
            # Weight the human winning really low
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else: # No more valid moves
                return (None, 0)
        # Return the bot's score
        else:
            return (None, score_position(board, BOT_PIECE))

    if maximisingPlayer:
        value = -math.inf
        # Randomise column to start
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            # Create a copy of the board
            b_copy = board.copy()
            # Drop a piece in the temporary board and record score
            drop_piece(b_copy, row, col, BOT_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                # Make 'column' the best scoring column we can get
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimising player
        value = math.inf
        # Randomise column to start
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            # Create a copy of the board
            b_copy = board.copy()
            # Drop a piece in the temporary board and record score
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                # Make 'column' the best scoring column we can get
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

'''
------------- Gameplay --------------
'''

# Initialise game
board = create_board()
game_over = False
turn = 0 # Human goes first

while not game_over:
    if turn == PLAYER:

        # Ask Human (Player 1) to choose a column
        col = int(input("Human player choose a column: "))

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_PIECE)

            if winning_move(board, PLAYER_PIECE):
                game_over = True
                print("Human Wins!")

            # Advance turn & alternate between Player 1 and 2
            turn += 1
            turn = turn % 2

    if turn == BOT and not game_over:

        # Ask Ro-Bot (Player 2) to pick the best move based on weighted scoring
        # col = pick_best_move(board, BOT_PIECE)

        # Ask Ro-Bot (Player 2) to pick the best move based on possible opponent future moves
        col, minimax_score = minimax(board, 4, -math.inf, math.inf, True) # A higher value takes longer to run

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, BOT_PIECE)

            if winning_move(board, BOT_PIECE):
                game_over = True
                print("Ro-Bot Wins!")

            # Advance turn & alternate between Player 1 and 2
            turn += 1
            turn = turn % 2

    print_board(board)

    # When game finishes, wait for 30 seconds
    if game_over:
        print('Game finished!')
