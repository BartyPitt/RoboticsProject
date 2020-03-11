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

.. note:: 

    Due to restrictions on the version of numpy, ``np.flipud(board)`` was used instead of the most up to date version: ``np.flip(board)``.
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

When the human player (Player 1) has made a move, the ``drop_piece`` function will update the numpy array ``board``. In order for the game algorithm to choose the best move to play in response, it has to understand and analyse the current board state. This is done using a 'windowing' technique.
In the following function, horizontal, vertical, positive (upward sloping) and negative (downward sloping) diagonal windows are created. These windows are then used to scan all possible 4-piece sections of the board, and evaluate (score) each window based on its contents. 
This evaluation is performed separately by the ``evaluate_window`` function, which is called within the ``score_position`` function, and explained in further detail below.

.. code-block:: python

    def score_position(board, piece):
        score = 0

        # Score centre column
        centre_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
        centre_count = centre_array.count(piece)
        score += centre_count * 3

        # Score horizontal positions
        for r in range(ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(COLUMN_COUNT - 3):
                # Create a horizontal window of 4
                window = row_array[c:c + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        # Score vertical positions
        for c in range(COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(ROW_COUNT - 3):
                # Create a vertical window of 4
                window = col_array[r:r + WINDOW_LENGTH]
                score += evaluate_window(window, piece)

        # Score positive diagonals
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                # Create a positive diagonal window of 4
                window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        # Score negative diagonals
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                # Create a negative diagonal window of 4
                window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += evaluate_window(window, piece)

        return score

The figure below shows the scanning range for this ``score_position`` function. It is unnecessary to use every index of the board as a starting position for a scanning window, because in many positions some windows would then extend over the sides of the board.
As a result, there are only 69 positions in which the scanning window needs to be deployed. The yellow highlight shows the applicable scanning range, and the red squares are an example of a scanning window in the maximum required position.

.. figure:: _static/scanning_windows.png
    :align: center
    :figclass: align-center



Algorithm
----------