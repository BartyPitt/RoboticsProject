Connect Four Algorithm
============================

In order for the robot to play competitively against a human, a game algorithm is used to choose the best move in response to the human player. The algorithm's 'game loop' is implemented inside the main file, but for general tidiness we store all of the functions in a separate file.


Functional Overview
---------------------

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
                # print("\033[40;38;5;82m Hello \033[30;48;5;82m World \033[0m")

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
    If you are using the most up to date version of numpy, you can update this function (although it will not break if you do not - numpy has reasonably good backwards-compatibility)