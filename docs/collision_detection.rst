Collision Detection
======================

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
