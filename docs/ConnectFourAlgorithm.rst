Connect Four Algorithm
============================

In order for the robot to play competitively against a human, a game algorithm is used to choose the best move in response to the human player. The algorithm's 'game loop' is implemented inside the main file, but for general tidiness we store all of the functions in a separate file.


Setup
----------

Create a numpy zeroes array to represent the Connect 4 board. This will be populated with pieces throughout the game.

.. code-block:: python

    def create_board():
        board = np.zeros((ROW_COUNT, COLUMN_COUNT))
        return board

Set up the board to print out in the terminal in a way that makes it visually easy to play with the computer.

.. code-block:: python

    def pretty_print_board(board):
        flipped_board = np.flipud(board)

        print("\033[0;37;41m 0 \033[0;37;41m 1 \033[0;37;41m 2 \033[0;37;41m 3 \033[0;37;41m 4 \033[0;37;41m 5 \033[0;37;41m 6 \033[0m")
        for i in flipped_board:
            row_str = ""

            for j in i:
                if j == 1:
                    #print(yellow)
                    row_str +="\033[0;37;43m 1 "
                elif j ==2:
                    row_str +="\033[0;37;44m 2 "
                else:
                    #print black
                    row_str +="\033[0;37;45m   "
                    
            print(row_str+"\033[0m")

.. note:: Due to restrictions on the version of numpy, ``np.flipud(board)`` was used instead of the most up to date version: ``np.flip(board)``.
    If you are using the most up to date version of numpy, you can update this function (although it will not break if you do not - numpy has reasonably good backwards-compatibility).
    The algorithm fills the board from the top down, whereas in real life the board fills up from the bottom. ``np.flipud(board)`` flips the board about a horizontal axis, making it the correct visual orientation for Connect 4.

There are 4 functions that are used when placing a piece on the board.

1. To get all locations in the board that could contain a piece (i.e. have not yet been filled):

.. code-block:: python

    def get_valid_locations(board):
        valid_locations = []
        for col in range(COLUMN_COUNT):
            if is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

2. To check if there is a valid location in the chosen column:

.. code-block:: python

    def is_valid_location(board, col):
        return board[ROW_COUNT - 1][col] == 0

3. To check which row the piece can be placed into (i.e. the next available open row):

.. code-block:: python

    def get_next_open_row(board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r

4. Finally, to place a piece in the next available row, in the chosen column:

.. code-block:: python

    def drop_piece(board, row, col, piece):
        board[row][col] = piece

Analysis
----------

Algorithm
----------