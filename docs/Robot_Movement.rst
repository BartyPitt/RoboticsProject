Robot Movement Overview
===============================

*"It would be good if the robot never did that again"*

*- Alattar, Ahmad*




Functional Overview
----------------------------------------


Init
^^^^

::

    def __init__(self, GripperSizeExtended=0.03, GripperSizeRetracted=0, group=moveit_commander.MoveGroupCommander(
        "panda_arm"), group2 = moveit_commander.MoveGroupCommander("hand")):
        ''' Sets up the Inital setup conditions for the robot.
        '''
        self.GripperSizeRetracted = GripperSizeRetracted
        self.GripperSizeExtended = GripperSizeExtended
        self.group = group # All joints apart from the grippers
        self.__positions__ = dict()  # the __ does nothing , it just signifies that I dont want the user to be writting to the memory location directly.
        self.group2 = group2 # Gripper joints

When an instance of the Connect4Robot is created, the method init() is automatically called. This defines the variables for opening and closing the gripper, which are used in their related methods. 2 groups are also created. These are "group", which includes all the joints in the arm of the robot and "group2", which includes the joints in the gripper. These are used by the moveit_commander library for moving the robot. Finally, a dictionary is initialised, which will be used for storing position names and cartesian coordinates.




AddPosition
^^^^^^^^^^^
::

	def AddPosition(self , PositionName , PositionCordinates):
			'''A setter function that sets up the positions for the robot to travel to'''
			self.__positions__[PositionName] = PositionCordinates

The function is designed to store a coordinate in cartesian form in a private dictionary. This function originally stored the variables in the form 
of a Moveit Pose class , this was later changed , as it is very difficult to both view the values as well as made it very difficult to modify the values.
The function remained partially to interact with legacy code, and partially as it was thought that it maybe useful to add in a sanitization layer.


Calibration
^^^^^^^^^^^

::

    def Calibration(self):
        ''' Calibration function to align board and test robot '''
    	raw_input("Press Enter to move to DiskCollection point...")
    	self.MoveToPosition("DiskCollection")
    	raw_input("Press Enter to open gripper...")
    	self.opengrip()
    	raw_input("Press Enter to close gripper...")
    	self.closegrip()
        raw_input("Press Enter to move to left corner...")
        self.moveto([self.x1, self.y1, self.z1, self.roll1, self.pitch1, self.yaw1])
        raw_input("Press Enter to continue to right corner...")
        self.moveto([self.x2, self.y2, self.z2, self.roll2, self.pitch2, self.yaw2])
        raw_input("Press Enter to continue to game...")

The calibration method has 2 purposes. The first is to check that the robot is operating correctly, which is done by making it move to a position and then open and close its gripper. The second is to enable the connect 4 board to be positioned correctly in the real world. This is done by making the Panda robot move its end effector to above where the 1st column on the board should be. Once the user has aligned the board beneath it, they should press Enter, and the end effector will move above the last column on the board. Since the exact height above the board is not important, this is enough to enable the board to be correctly positioned.


Define coordinates
^^^^^^^^^^^^^^^^^^
::

    def define_coordinates(self, LeftCorner, dx=0, dy=-0.468, dz=0):
        '''Defines top left corner of board (from pov of robot) relative to the robot and moves to calibration points'''
        [x, y, z, roll, pitch, yaw] = LeftCorner
        RightCorner = [x + dx, y + dy, z + dz, roll, pitch, yaw]
        self.__positions__["LeftCorner"] = LeftCorner
        self.__positions__["RightCorner"] = RightCorner

        [self.x1, self.y1, self.z1, self.roll1, self.pitch1, self.yaw1] = LeftCorner
        [self.x2, self.y2, self.z2, self.roll2, self.pitch2, self.yaw2] = RightCorner


This method enables us to reposition the board if we need to, as long as it remains perpendicular to the robot. We define where the left corner is going to be (as seen by the robot), and the right corner is automatically calculated. The coordinates of the left and right corners are then created as attributes so that all other positions in cartesian space can be defined relative to the board, and will auto-update if we change the location of the board. Being able to reposition the board is important so that we can test different places in the robot's task space which lead to more reliable motion planning.




Coordinates to pose
^^^^^^^^^^^^^^^^^^^

::

    def CordinatesToPose(self, Position):
        '''Takes in a cordinate and transforms it into a pose'''
        x, y, z, roll, pitch, yaw = Position
        quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)

        pose = geometry_msgs.msg.Pose()
        pose_o = pose.orientation
        pose_o.x, pose_o.y, pose_o.z, pose_o.w = quaternion
        # Defining target coordinates
        pose.position.x = x
        pose.position.y = y
        pose.position.z = z
        return pose

The human-legible cartesian position coordinates (x,y,z) as well as the Euler angles (roll, pitch, yaw) must be converted into a different coordinate space which can be understood by the robot motion planner. This starts by converting the Euler angles into quaternions and then converting these orientations as well as the Cartesian positions into a format understood by the moveit_controller library.


Neutral
^^^^^^^

::

    def neutral(self):
        ''' Moves to disk collection position using joint angles.
            Joint angles used so that the robot doesn't work itself into singularity. '''

    	self.movejoints([0.963,0.264,0.117,-1.806,-0.035,2.063,0.308])


A challenge faced with the robot was that throughout the game it would slowly work itself into a singularity position after various successive moves, which meant it would become unable to move. In order to avoid this, a reset stage was required that would reconfigure the robot joints to a specific position after each move. Neutral() is a method which achieves this. It instructs the robot to move into a particular set of joint positions which orient it off to the side of the board. This method can be called after each time the robot plays a move, and can be used as the position from which it collects a disk.


Cartesian Path
^^^^^^^^^^^^^^
::

	def CartesianPath(self, Endposition , StartPosition = None , max_tries = 10):
		'''Takes an Endpositions and generates and then acts on a motion plan to the Endposition using compute cartesian path. '''
		if StartPosition:
			StartPosition = self.CordinatesToPose(StartPosition)
		else:
			StartPosition = group.get_current_pose().pose
		
	    Endposition = self.CordinatesToPose(Endposition)
		
	    waypoints = []
		# start with the current pose
	    waypoints.append(StartPosition)
		
		
	    waypoints.append(Endposition)
	    for i in range(max_tries):
			(plan, fraction) = group.compute_cartesian_path (
									waypoints,   # waypoint poses
									0.01,        # eef_step
									0.0,         # jump_threshold
									True)        # avoid_collisions
			if fraction == 1:
				print("Motioned Planned Successfully")
				break
	    else:
			print("failed to run")
			return False

	    self.group.execute(plan , wait = True)
	    self.group.clear_pose_targets()
	    return True





Gripper Control
---------------------
We had two options for controlling the gripper, one by using movit commander's ``go(joint_goal, wait=True)`` function to move the gripper to the target location and using the ``GraspGoal(width=0.015,speed=0.08,force=1)`` function. Each had its drawbacks.


Using GraspGoal() function
------------------------------

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


Using go() function
------------------------------

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







Current Order of Called Functions.::

*PLease PlAcE aN ImagE HerE*


