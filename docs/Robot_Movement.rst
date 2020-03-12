Robot Motion
===============================

We used the default motion planner in Movit, which uses the OMPL, an open-source motion planning library that primarily implements randomized motion planners.
A separate python script was created which contained the robot class with methods related to its motion. This enabled us to keep the main python script clean and legible. The following in a breakdown of the methods within this Connect4Robot class.


Init
----------

When an instance of the Connect4Robot is created, the method init() is automatically called. This defines the variables for opening and closing the gripper, which are used in their related methods. 2 groups are also created. These are "group", which includes all the joints in the arm of the robot and "group2", which includes the joints in the gripper. These are used by the moveit_commander library for moving the robot. Finally, a dictionary is initialised, which will be used for storing position names and cartesian coordinates.

.. code-block:: python

    def __init__(self, GripperSizeExtended=0.03, GripperSizeRetracted=0, group=moveit_commander.MoveGroupCommander(
        "panda_arm"), group2 = moveit_commander.MoveGroupCommander("hand")):
        ''' Sets up the Inital setup conditions for the robot.
        '''
        self.GripperSizeRetracted = GripperSizeRetracted
        self.GripperSizeExtended = GripperSizeExtended
        self.group = group # All joints apart from the grippers
        self.__positions__ = dict()
        self.group2 = group2 # Gripper joints


Calibration
------------------------

The calibration method has 2 purposes. The first is to check that the robot is operating correctly, which is done by making it move to a position and then open and close its gripper. The second is to enable the connect 4 board to be positioned correctly in the real world. This is done by making the Panda robot move its end effector to above where the 1st column on the board should be. Once the user has aligned the board beneath it, they should press Enter, and the end effector will move above the last column on the board. Since the exact height above the board is not important, this is enough to enable the board to be correctly positioned.

.. code-block:: python

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



Define coordinates
---------------------


This method enables us to reposition the board if we need to, as long as it remains perpendicular to the robot. We define where the left corner is going to be (as seen by the robot), and the right corner is automatically calculated. The coordinates of the left and right corners are then created as attributes so that all other positions in cartesian space can be defined relative to the board, and will auto-update if we change the location of the board. Being able to reposition the board is important so that we can test different places in the robot's task space which lead to more reliable motion planning.

.. code-block:: python

    def define_coordinates(self, LeftCorner, dx=0, dy=-0.468, dz=0):
        '''Defines top left corner of board (from pov of robot) relative to the robot and moves to calibration points'''
        [x, y, z, roll, pitch, yaw] = LeftCorner
        RightCorner = [x + dx, y + dy, z + dz, roll, pitch, yaw]
        self.__positions__["LeftCorner"] = LeftCorner
        self.__positions__["RightCorner"] = RightCorner

        [self.x1, self.y1, self.z1, self.roll1, self.pitch1, self.yaw1] = LeftCorner
        [self.x2, self.y2, self.z2, self.roll2, self.pitch2, self.yaw2] = RightCorner



AddPosition
-------------

This function is designed to store a coordinate in cartesian form in a private dictionary. It originally stored the variables in the form
of a Moveit Pose class, however this was later changed, as it is very difficult to both view the values as well as making it very difficult to modify the values.
The function remained partially to interact with legacy code, and partially as it was thought it might be useful to add in a sanitization layer.

.. code-block:: python

	def AddPosition(self , PositionName , PositionCordinates):
			'''A setter function that sets up the positions for the robot to travel to'''
			self.__positions__[PositionName] = PositionCordinates


Interpolation
---------------


This function was used to generate the coordinates of the columns. Interpolation was used as a method to avoid hard coding the column coordinates individually, and is used when the AddPosition method is called in the main function.

.. code-block:: python

        def interpolation(self, column):
        ydistance = (self.y2-self.y1)/6 * (column-1)
        return self.y1 + ydistance


Move to
-------------

This is a movement function that uses the moveit motion planner to move the robot.
It takes in a position in cartesian list form, transforms it into the pose class, and then runs it directly through the motion planner.
It then executes the plan.

.. code-block:: python

    def moveto(self, Position):
        '''Moves to a given position, in form [x,y,z,roll,pitch,yaw]'''

        # print("Moving to: ({},{},{}) with angle ({:.2f},{:.2f},{:.2f})".format(*Position))

        # Converting the roll, pitch, yaw values to values which "moveit" understands
        pose_goal = self.CordinatesToPose(Position)

        self.group.set_pose_target(pose_goal)  # Set new pose objective
        plan = self.group.go(wait=True)  # Move to new pose
        rospy.sleep(0.5)
        # It is always good to clear your targets after planning with poses.
        self.group.clear_pose_targets()


Coordinates to pose
-----------------------

The human-legible cartesian position coordinates and rotations  (x, y, z, roll, pitch, yaw), must be passed into a class for moveit to be able to interpret them.
This starts by converting roll, pitch and yaw angles into quaternions and then converting these orientations as well as the Cartesian positions
into a format understood by the moveit_controller library.

.. code-block:: python

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


Move To Position
-------------------


The function takes the name of a position and moves the robot to that position. It enabled us to feed in the position names defined in main.py.

.. code-block:: python

        def MoveToPosition(self ,Position):
            '''Takes the name of the position and moves the robot to that position.'''
            Cordinates = self.__positions__[Position]
            self.moveto(Cordinates)

Move joints
-----------------
This is the command for direct joint control of the robot. For the most part the use of motion planners and inverse kinematics was preferred for this project.
Most of the motion planning was done with the moveto() and the MoveToPosition() commands.
This function was added so that after every run the robot could head to a set joint position, the idea behind this being that it stopped the robot from gradually working
its way into a singularity, something that would happen within the simulations.


.. code-block:: python

    def movejoints(self, jointAngles):
        '''Takes in joint angles and moves to that pose'''
        joint_goal = self.group.get_current_joint_values()
        joint_goal = jointAngles
        self.group.go(joint_goal, wait=True)
        self.group.stop()


Neutral
------------


Throughout the game the robot would slowly work itself into a singularity position after various successive moves, which meant it would become unable to move. In order to avoid this, a reset stage was required that would reconfigure the robot joints to a specific position after each move. Neutral() is a method which achieves this. It instructs the robot to move into a particular set of joint positions which orient it off to the side of the board. This method can be called after each time the robot plays a move, and can be used as the position from which it collects a disk.

.. code-block:: python

    def neutral(self):
        ''' Moves to disk collection position using joint angles.
            Joint angles used so that the robot doesn't work itself into singularity. '''

        self.movejoints([0.963,0.264,0.117,-1.806,-0.035,2.063,0.308])



Cartesian Path
------------------

Cartesian path is a function that takes in an Endposition for the robot to move to and uses the compute_cartesian_path() function to generate a cartesian path between the two.
This function was useful, since for the most part it would keep the robot end effector along an easily predictable path. This gives much more stability than moveto(). The main difference
between the two functions other than the motion planning is that Cartesian Path returns a true or false depending on weather or not it was successful.


.. code-block:: python

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



Robot Initialisation
------------------------


Standard procedure, to clear the current targets to avoid conflicts.


.. code-block:: python

    def robot_init(self):
        ''' Clears targets, good to do after planning poses '''
        self.group.clear_pose_targets()


Gripper Control
---------------------
We had two options for controlling the gripper, one by using movit commander's ``go(joint_goal, wait=True)`` function to move the gripper to the target location and using the ``GraspGoal(width=0.015,speed=0.08,force=1)`` function. Each had its drawbacks.


Using GraspGoal() function
------------------------------

When picking up the ConnnectFour token, ideally we would control both the position of gripper as well as the force it exerts. We do not want to exceed the maximum force that the gripper can produce, but we must ensure the token doesn't fall off due to a lack of force. We therefore tried using the ``GraspGoal(width=0.015,speed=0.08,force=1)`` function to set the gripper in place and exert a force on the token such that it did not fall off. However, we discovered that it would grip it, and then release its grip as soon as the ``closegrip()`` function came to an end. We could not figure out why it kept relaxing its grip.


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
-----------------------


What worked in the end was DIRECTLY setting the gripper position to the fully closed postion by setting both gripper's position to ``0.0``. However, there was a good chance of failure when using this method. We set the gripper's position to ``0`` despite the connect 4 token stopping it being able to achieve this goal. The robot could have thrown an error, however we discovered that due to the small size of the token and the flexiblity of the gripper pads, the grippers could close fully without detecting the ConnectFour token obstacle.


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




Note that we have a separate function that broadcasts the gripper position to ROS. This is to ensure Gazebo sees the movement and displays accordingly. We create a ``gripper_publisher`` that publishes the new gripper position to the ``/franka/gripper_position_controller/command`` topic so that Gazebo can be updated.
