#!/usr/bin/env python

class Connect4Robot():

	def __init__(self,GripperSizeExtended = 0.05 , GripperSizeRetracted = 0): #defult positions added to maintain compability with legacy code
		'''Sets up the Inital setup conditions for the robot.
		TODO add in more setup conditions when more are needed.
		'''
		self.GripperSizeRetracted = GripperSizeRetracted
		self.GripperSizeExtended = GripperSizeExtended
		self.__positions__ = dict() #the __ does nothing , it just signifies that I dont want the user to be writting to the memory location directly.
	
	def AddPosition(self , PositionName , PositionCordinates):
		'''A setter funciton that sets up the positions for the robot to travel to'''
		self.__positions__[PositionName] = PositionCordinates
	
	def MoveToPosition(self ,Position):
		'''Takes the name of the position and moves the robot to that position.'''
		Cordinates = self.__positions__[Position]
		self.moveto(*Cordinates)


	def moveto(self,x,y,z,roll,pitch,yaw):
		print("Moving to: ({},{},{}) with angle ({:.2f},{:.2f},{:.2f})".format(x,y,z,roll,pitch,yaw))
		#Converting the roll, pitch, yaw values to values which "moveit" understands
		quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)

		pose_goal = geometry_msgs.msg.Pose() # Sets var to current pose, just to get the variable in the correct format

		# Defining target angle
		pose_goal.orientation.x = quaternion[0]
		pose_goal.orientation.y = quaternion[1]
		pose_goal.orientation.z = quaternion[2]
		pose_goal.orientation.w = quaternion[3]
		# Defining target coordinates
		pose_goal.position.x = x
		pose_goal.position.y = y
		pose_goal.position.z = z

		group.set_pose_target(pose_goal) # Set new pose objective
		plan = group.go(wait=True) # Move to new pose
		rospy.sleep(2)
		# It is always good to clear your targets after planning with poses.
		group.clear_pose_targets()

	def movejoints(self, joint1, joint2, joint3, joint4, joint5, joint6, joint7):
		'''Takes in joint angles and moves to that pose'''
		joint_goal = group.get_current_joint_values()
		joint_goal = [joint1, joint2, joint3, joint4, joint5, joint6, joint7]
		group.go(joint_goal, wait=True)
		group.stop()


	def closegrip(self, simulation=True, GripOveride=None):
	    if simulation:
			if GripOveride == None:
				GripOveride = self.GripperSizeRetracted
			gripper_msg.data = [GripOveride, GripOveride]
			gripper_publisher.publish(gripper_msg)
			rospy.sleep(2)
	    else:
	        group2 = moveit_commander.MoveGroupCommander("hand")
	        joint_goal = group2.get_current_joint_values()
	        joint_goal[0] = self.GripperSizeRetracted
	        joint_goal[1] = self.GripperSizeRetracted

	        group2.go(joint_goal, wait=True)
	        group2.stop()

	def opengrip(self, simulation=True, GripOveride=None):
	    if simulation:
			if GripOveride == None:
				GripOveride = self.GripperSizeExtended
			gripper_msg.data = [GripOveride, GripOveride]
			gripper_publisher.publish(gripper_msg)
			rospy.sleep(2)
	    else:
	        group2 = moveit_commander.MoveGroupCommander("hand")
	        joint_goal = group2.get_current_joint_values()
	        joint_goal[0] = self.GripperSizeExtended
	        joint_goal[1] = self.GripperSizeExtended

	        group2.go(joint_goal, wait=True)
	        group2.stop()


