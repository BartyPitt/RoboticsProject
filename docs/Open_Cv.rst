Open CV Overview
===============================
OpenCV is used as a way to allow the robot to update the state of the board and know where the human has played without requiring any inputs.
It is also used for error prevention and recovery, as will be further explained.

System Overview for Counter position detection.
--------------------------------------------------

This code is called by the decision making algorithm when it needs to know the current position of the placed counters

In the game of connect 4 counters are placed into columns inside of the grid. One of the major tasks for machine vision is figuring out the current position of the counters in play.

Currently the algorithm for counter detection can be split into five separate stages.

1. The webcam currently attached to the system takes a picture of the board in its current state
2. The machine vision detects the four corners of the connect 4 grid.
3. The system warps the image so that just the connect 4 grid is shown in a planer projection.
4. The image detects the position of all the counters in play and calculates in which column each of the counters falls into.
5. The location of all the counters is returned in the form of a numpy array

Current Order of Called Functions.::

*PLease PlAcE aN ImagE HerE*


Mask and Contour Function
----------------------------------------
