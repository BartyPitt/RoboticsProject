Open CV Overview
===============================

*"You sure you need a Camera"*

*- Petar*

In order for the robot to be able to play connect 4 basic sets of machine vision *algorythems* were implimented.


System Overview for Counter position detection.
----------------------------------------

This code is called by the decsion making algorythem when it needs to know the current posstion of the placed counters

In the game of connect 4 counters are placed into columns inside of the grid. One of the major tasks for machine vision is figuring out the current position of the counters in play.

Currently the *alogrythm* for counter detection can be split into five seperate stages.

1. The webcam currently attached to the system takes a picture of the board in its current state
2. The machine vision detects the four corners of the connect 4 grid.
3. The system warps the image so that just the connect 4 grid is shown in a planer projection.
4. The image detects the positon of all the counters in play and calculates in which column each of the counters falls into.
5. The location of all the counters is returned in the form of a numpy array

Current Order of Called Functions.::

*PLease PlAcE aN ImagE HerE*


Mask and Countour Function
----------------------------------------









