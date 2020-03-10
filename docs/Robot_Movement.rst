Robot Movement Overview
===============================

We have control over the 7 joints of the panda robot as well as the two grippers. 


Gripper
^^^^^^^^^^^^^
We had two options for controlling the gripper, one by using movit commander's ``go(joint_goal, wait=True)`` function to move the gripper to the target location and using the ``GraspGoal(width=0.015,speed=0.08,force=1)`` function. Each had its drawbacks.



When picking up the ConnnectFour token, ideally, we would want to control both the position of gripper as well as the force exerted on it. We do not want to exceed the maximum force that the gripper can produce while preventing the token from falling off due to too little force exerted. We therefore tried using the ``GraspGoal(width=0.015,speed=0.08,force=1)`` function to set the gripper in place and exert a force on the token such that it did not fall off. However, we discovered that it would grip it, and then release its grip as soon as the ``closegrip()`` function came to an end. We could not figure out why it kept relaxing its grip.


.. code-block:: python
   :emphasize-lines: 8

	from franka_gripper.msg import GraspAction, GraspGoal

		def closegrip(self, simulation=False, GripOveride=None):
		    rospy.init_node('Franka_gripper_grasp_action')
		    client = actionlib.SimpleActionClient('/franka_gripper/grasp', GraspAction)
		    rospy.loginfo("CONNECTING")
		    client.wait_for_server()
		    action = GraspGoal(width=0.015,speed=0.08,force=1)
		    rospy.loginfo("SENDING ACTION")
		    client.send_goal(action)
		    client.wait_for_result(rospy.Duration.from_sec(5.0))
		    rospy.loginfo("DONE")



What worked in the end was DIRECTLY setting the gripper position to the fully closed postion by setting both gripper's position to ``0.0``. However, there was a good chance of failure when using this method. We set the gripper's position to ``0`` while there is an obstacle, the connectFour token in the way of the gripper fully closing. The robot could have thrown an error. However, we discovered that due to the small size of the token and the flexiblity of the gripper pads, the grippers could close fully without detecting the ConnectFour token obstacle. 


The code for closing the gripper is as follows

.. code-block:: python
   :emphasize-lines: 6


	def closegrip(self, simulation=False, GripOveride=None):
	    ''' Function to open the grip of the robot '''
	    joint_goal = self.group2.get_current_joint_values()
	    joint_goal[0] = 0.0
	    joint_goal[1] = 0.0
	    self.group2.go(joint_goal, wait=True)
	    self.group2.stop()
	    if simulation == True:
	        # For Gazebo simulation
	        if GripOveride == None:
	        	GripOveride = self.GripperSizeExtended
	        gripper_publisher = rospy.Publisher('/franka/gripper_position_controller/command', Float64MultiArray,queue_size=1)
	        gripper_msg = Float64MultiArray()
	        gripper_msg.layout.dim = [MultiArrayDimension('', 2, 1)]
	        gripper_msg.data = [GripOveride, GripOveride]
	        gripper_publisher.publish(gripper_msg)
	        rospy.sleep(0.5)




Note that we have a seperate function that broadcasts the gripper position to ROS. This is to ensure Gazebo sees the movement and displays accordingly. We create a ``gripper_publisher`` that publishes the new gripper position to the ``/franka/gripper_position_controller/command`` topic so that Gazebo can be updated.