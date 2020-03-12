Collision Detection
======================

Throughout the project , collision detection has been implemented by placing the obstacle geometry directly into the moveit scene.
The reason for this is that by placing it into the Moveit scene it connects directly to the motion planning. 
Originally an simplified stl model of the board was placed inside the environment.
This was replaced with just a large cuboid over the area that would be taken up by the grid, as it significantly reduced the computation time for motion planning.

