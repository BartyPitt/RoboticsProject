Motion planning
======================


We used the default motion planner in Movit, which uses the OMPL, an open-source motion planning library that primarily implements randomized motion planners.




Collision Avoidance
--------------------------
The primary obstacle in the robot's workspace was the Connect 4 board. We had to tell Movit, the motion planner, to avoid getting any part of the robot to collide with the board. 

Two accurate models were required for collision detection. I 3D model of the robot, including all its links and of the connect 4 board.


In order to simplify computation, we defined the obstacle solely by a bounding box, a box that completely encompassed the volume of the connect 4 board.



.. code-block:: python

	p = geometry_msgs.msg.PoseStamped()
	#p = PoseStamped()
	p.header.frame_id = robot.get_planning_frame()
	p.pose.position.x = 0.4
	p.pose.position.y = -0.301298
	p.pose.position.z = -0.2
	p.pose.orientation.x =  0.0
	p.pose.orientation.y = 0
	p.pose.orientation.z = 0.0
	p.pose.orientation.w = 0.4440158
	#scene.add_mesh("Connect4", p,"connect4.STL")
	scene.add_box("table", p, (0.5, 1.5, 0.6))
	rospy.sleep(2)

Throughout the project , collision detection has been implemented by placing the obstacle geometry directly into the moveit scene.
The reason for this is that by placing it into the Moveit scene it connects directly to the motion planning. 
Originally an simplified stl model of the board was placed inside the environment.
This was replaced with just a large cuboid over the area that would be taken up by the grid, as it significantly reduced the computation time for motion planning.

.. figure:: _static/Rviz_obstacle.png
    :align: center
    :figclass: align-center

