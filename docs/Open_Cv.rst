Open CV Overview
===============================
OpenCV is used to allow the robot to update the state of the board and know where the human has played without requiring any inputs.
It is also used for error prevention and recovery, as will be further explained.

System Overview for Counter position detection:
--------------------------------------------------

This code is called by the decision making algorithm when it needs to know the current position of the placed counters.

In the game of connect 4 counters are placed into columns inside of the grid. One of the major tasks for machine vision is figuring out the current position of the counters in play.

It then needs to find the new counter that has been placed in the board by the human.

Currently the algorithm for counter detection can be split into five separate stages:

1. The webcam currently attached to the system takes a picture of the board in its current state.
2. The machine vision detects the four corners of the connect 4 grid.
3. The system warps the image so that just the connect 4 grid is shown in a planer projection.
4. The image detects the position of all the counters in play and calculates in which column each of the counters falls into.
5. The location of all the counters is returned in the form of a numpy array. This is saved as board1

These steps are then repeated again. This outputs another board state in the form of a numpy array, saved as board2. Then board1 is subtracted from board2 to find where the new counter is.

The column and the row of the new counter are found and the column is returned to the connect 4 playing algorithm to continue the game.

How the code works:
--------------------------------------------------



Error detection with OpenCV:
--------------------------------------------------
