#!/usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf
from math import pi
from std_msgs.msg import String, Float64MultiArray, MultiArrayDimension, Float64
from moveit_commander.conversions import pose_to_list

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

	def interpolation(self, column):
		ydistance = (self.y2-self.y1)/6 * (column-1)
		return self.y1 + ydistance


	def Calibration(self , LeftCorner,dx = 0 , dy = -0.468 , dz = 0):
		''''''
		[x,y,z,roll,pitch,yaw] = LeftCorner 
		RightCorner = [x+dx,y+dy,z+dz,roll,pitch,yaw]
		self.__positions__["LeftCorner"] = LeftCorner
		self.__positions__["RightCorner"] = RightCorner
		[self.x1 ,self.y1 ,self.z1 ,self.roll1 ,self.pitch1 ,self.yaw1]    = LeftCorner
		[self.x2 , self.y2 , self.z2 , self.roll2 , self.pitch2, self.yaw2] = RightCorner

		self.moveto([self.x1,self.y1,self.z1,self.roll1,self.pitch1,self.yaw1])
		sleep(5)
		self.moveto([self.x2,self.y2,self.z2,self.roll2,self.pitch2,self.yaw2])
		sleep(5)
	
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

	def closegrip(self , GripOveride = None):
		if GripOveride == None:
			GripOveride = self.GripperSizeRetracted
		gripper_msg.data = [GripOveride, GripOveride]
		gripper_publisher.publish(gripper_msg)
		rospy.sleep(2)

	def opengrip(self, GripOveride = None):
		if GripOveride == None:
			GripOveride = self.GripperSizeExtended
		gripper_msg.data = [GripOveride, GripOveride]
		gripper_publisher.publish(gripper_msg)
		rospy.sleep(2)




if __name__=="__main__":

	# Setting-up processes

	moveit_commander.roscpp_initialize(sys.argv)
	rospy.init_node('panda_demo', anonymous=True)
	robot = moveit_commander.RobotCommander()
	scene = moveit_commander.PlanningSceneInterface()
	group = moveit_commander.MoveGroupCommander("panda_arm")
	gripper_publisher = rospy.Publisher('/franka/gripper_position_controller/command', Float64MultiArray, queue_size=1)
	gripper_msg = Float64MultiArray()
	gripper_msg.layout.dim = [MultiArrayDimension('', 2, 1)]

	PandaRobot = Connect4Robot()
	# Calibration positions
	PandaRobot.closegrip()
	PandaRobot.Calibration([0.3, 0.35, 0.3, pi,0,pi/4])


	PandaRobot.AddPosition("DiskCollection" ,[PandaRobot.x1,PandaRobot.y1 + 0.2 ,PandaRobot.z1 + 0.1,PandaRobot.roll1,PandaRobot.pitch1,PandaRobot.yaw1])
	PandaRobot.AddPosition("AboveBoard" , [PandaRobot.x1,PandaRobot.y1,PandaRobot.z1,PandaRobot.roll1,PandaRobot.pitch1,PandaRobot.yaw1])
	for i in range(1,7):
		PandaRobot.AddPosition(str(i) ,[PandaRobot.x1,PandaRobot.y1 - PandaRobot.interpolation(i),PandaRobot.z1,PandaRobot.roll1,PandaRobot.pitch1,PandaRobot.yaw1])

	#PandaRobot.CartesianPath([0.5, 0.347412681245, 0.65, pi,0,pi/4])
	#PandaRobot.CartesianPath([0.5, -0.118074733645, 0.65, pi,0,pi/4])

	# # Main code
	PandaRobot.opengrip()
	for i in range(14):
	 	PandaRobot.MoveToPosition("DiskCollection")
	 	PandaRobot.closegrip()
		PandaRobot.MoveToPosition("AboveBoard")
		PandaRobot.MoveToPosition("1")
		PandaRobot.opengrip()
	