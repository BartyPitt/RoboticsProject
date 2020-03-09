#!/usr/bin/env python

from std_msgs.msg import String, Float64MultiArray, MultiArrayDimension, Float64
import sys
import rospy
import tf
import moveit_msgs.msg
import geometry_msgs.msg
import moveit_commander
from std_msgs.msg import String, Float64MultiArray, MultiArrayDimension, Float64
from moveit_commander.conversions import pose_to_list



def MultiVaribleInterpolation(Point1 , Point2 , Percent):
	'''Multi variable linear interpolation between two points using a percent.'''
	Output = []
	for Chord1 , Chord2 in zip(Point1,Point2):
		Output.append(Chord1 + (Chord1 - Chord2) * Percent)
	return Output


class Connect4Robot():

	def __init__(self,GripperSizeExtended = 0.03 , GripperSizeRetracted = 0, group = None): #defult positions added to maintain compability with legacy code
		'''Sets up the Inital setup conditions for the robot.
		TODO add in more setup conditions when more are needed.
		'''
		moveit_commander.roscpp_initialize(sys.argv)
		rospy.init_node('panda_demo', anonymous=True)
		self.robot = moveit_commander.RobotCommander()
		self.scene = moveit_commander.PlanningSceneInterface()
		self.GripperSizeRetracted = GripperSizeRetracted
		self.GripperSizeExtended = GripperSizeExtended
		if group == None:
			self.group = moveit_commander.MoveGroupCommander("panda_arm")
		else:
			self.group = group
		self.__positions__ = dict() #the __ does nothing , it just signifies that I dont want the user to be writting to the memory location directly.
		display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory,queue_size=20)
	
	def AddPosition(self , PositionName , PositionCordinates):
		'''A setter function that sets up the positions for the robot to travel to'''
		self.__positions__[PositionName] = PositionCordinates

	def interpolationPercentGen(self, column):
		Ydistance = (100)/6 * (column-1)
		return Ydistance
	
	def MultiVaribleInterpolationPanda(self, Name1 , Name2 , Percent):
		return MultiVaribleInterpolation(self.__positions__[Name1] , self.__positions__[Name2] , Percent)


	def Calibration(self , LeftCorner,dx = 0 , dy = -0.468 , dz = 0):
		'''Defines top left corner or board (relative to robot) and moves to calibration points'''
		[x,y,z,roll,pitch,yaw] = LeftCorner 
		RightCorner = [x + dx,y + dy,z + dz,roll,pitch,yaw]

		self.__positions__["LeftCorner"] = LeftCorner
		self.__positions__["RightCorner"] = RightCorner

		self.moveto(LeftCorner)
		rospy.sleep(5)
		self.moveto(RightCorner)
		rospy.sleep(5)
	
	def MoveToPosition(self ,Position):
		'''Takes the name of the position and moves the robot to that position.'''
		Cordinates = self.__positions__[Position]
		self.CartesianPath(Cordinates)


	def PoseToCordinates(self , Position):
		Po = Position.orientation
		roll,pitch,yaw = tf.transformations.euler_from_quaternion([Po.x,Po.y,Po.z,Po.w])
		x = Position.position.x
		y = Position.position.y
		z = Position.position.z
		return [x,y,z,roll,pitch,yaw]

	def CordinatesToPose(self,Position):
		'''Takes in a cordinate and transforms it into a pose'''
		x,y,z,roll,pitch,yaw = Position
		quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)
		
		pose = geometry_msgs.msg.Pose()
		pose_o = pose.orientation
		pose_o.x , pose_o.y , pose_o.z, pose_o.w = quaternion
		# Defining target coordinates
		pose.position.x = x
		pose.position.y = y
		pose.position.z = z
		return pose


	def moveto(self,Position): #position in form [x,y,z,roll,pitch,yaw]
		'''Moves to a given position'''
		print("Moving to: ({},{},{}) with angle ({:.2f},{:.2f},{:.2f})".format(*Position))
		#Converting the roll, pitch, yaw values to values which "moveit" understands
		pose_goal = self.CordinatesToPose(Position)

		self.group.set_pose_target(pose_goal) # Set new pose objective
		plan = self.group.go(wait=True) # Move to new pose
		rospy.sleep(2)
		# It is always good to clear your targets after planning with poses.
		self.group.clear_pose_targets()

	def movejoints(self, jointAngles):
		'''Takes in joint angles and moves to that pose'''
		joint_goal = self.group.get_current_joint_values()
		joint_goal = jointAngles
		self.group.go(joint_goal, wait=True)
		self.group.stop()

	def CartesianPath(self, Endposition , StartPosition = None,SubPoints = 50):

		if StartPosition:
			StartPosition = self.CordinatesToPose(StartPosition)
		else:
			StartPosition = self.group.get_current_pose().pose
		
		
		StartPosition = self.PoseToCordinates(StartPosition)
		print("Start Possition" , StartPosition)
		print("end Pos", Endposition)
		waypoints = []
		# start with the current pose
		for i in range(SubPoints + 1):
			Percent = i/SubPoints
			waypoints.append(self.CordinatesToPose(MultiVaribleInterpolation(StartPosition,
																			Endposition,
																			Percent)))

		max_tries = 10
		for i in range(max_tries):
			(plan, fraction) = self.group.compute_cartesian_path (
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


	def closegrip(self, simulation=True, GripOveride=None):
		if simulation:
			if GripOveride == None:
				GripOveride = self.GripperSizeRetracted
			gripper_publisher = rospy.Publisher('/franka/gripper_position_controller/command', Float64MultiArray, queue_size=1)
			gripper_msg = Float64MultiArray()
			gripper_msg.layout.dim = [MultiArrayDimension('', 2, 1)]
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
			gripper_publisher = rospy.Publisher('/franka/gripper_position_controller/command', Float64MultiArray, queue_size=1)
			gripper_msg = Float64MultiArray()
			gripper_msg.layout.dim = [MultiArrayDimension('', 2, 1)]
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

