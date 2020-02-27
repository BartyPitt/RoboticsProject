# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# SNAPSHOT CODE TO TAKE IMAGE1 AND IMAGE2 AT AN INTERVAL

#REMEMBER THAT BOARD WILL NOT BE FULL WITH DISKS, SO NEED TO ACCOUNT FOR EMPTY SLOTS
import numpy as np

EMPTY = 0
PLAYER_PIECE = 1
BOT_PIECE = 2

ROW_COUNT = 6
COLUMN_COUNT = 7

# =============================================================================
#UNCOMMENT TO TEST FUNCTIONS
# def create_board():
#     board = np.zeros((ROW_COUNT, COLUMN_COUNT))
#     return board
# 
# def drop_piece(board, row, col, piece):
#     board[row][col] = piece
#     return board
# =============================================================================

def disks_to_array(board):
    '''this function takes in the positions of all the disks on the board and returns a numpy
    array with -1 for the bot disks and 1 for the player disks'''
        
    for x in np.nditer(board, op_flags=['readwrite']):
        if x[...] == 1:
            x[...] = -1
        if x[...] == 2:
            x[...] = 1
    return board

def where_is_the_new_disk(board1, board2):
    '''this function takes in the board state before the human plays (board1) and after they play
    (board2), and subtracts them from each other. Where the result is not 0 it returns the column 
    and row of that position, which is where the new disk has been played'''
    board_before = disks_to_array(board1)
    board_after = disks_to_array(board2)
    result = np.subtract(board_before, board_after)
    for x in np.nditer(result):
        if x[...] != 0:
            i, j = np.where(result != 0)
    return i, j
    
# =============================================================================
#UNCOMMENT TO TEST FUNCTIONS
# board1 = create_board()
# board1 = drop_piece(board1, 3, 4, BOT_PIECE)
# 
# board2 = board1.copy()
# board2 = drop_piece(board2, 3, 5, PLAYER_PIECE)#row_of_new_disk, col_of_new_disk = where_is_the_new_disk(board1, board2)    
# =============================================================================
