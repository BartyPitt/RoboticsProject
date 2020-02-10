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

	def movejoints(self, joint1, joint2, joint3, joint4, joint5, joint6, joint7, finger_joint1, finger_joint2):
		'''Takes in joint angles and moves to that pose'''
		joint_goal = [joint1, joint2, joint3, joint4, joint5, joint6, joint7, finger_joint1, finger_joint2]
		group.go(joint_goal, wait=True)
		group.stop()

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
	PandaRobot.AddPosition("Neutral" ,[ 0.3,0.4,0.7,pi,0,pi/4])
	PandaRobot.AddPosition("DiskCollection" ,[0.3,0.4,0.15,pi,0,pi/4])
	PandaRobot.AddPosition("AboveBoard" , [0.6,0,0.7,pi,0,pi/4])
	PandaRobot.AddPosition("Column1" ,[0.6,0,0.64,pi,0,pi/4])


	# Calibration positions

	movejoints(0.5945, 0.4944, -0.09639, -1.2919, 0.0286, 1.8412, -0.2622, 3.2505e-05, 3.2505e-05)
	sleep(5)
	movejoints(-0.0336, 0.2612, -0.1809, -1.6607, 0.01549, 1.9535, -0.9906, 3.2505e-05, 3.2505e-05)
	sleep(5)

	# Main code

	for i in range(1):
		PandaRobot.MoveToPosition("Neutral")
		PandaRobot.opengrip()
		PandaRobot.MoveToPosition("DiskCollection")
		PandaRobot.closegrip()
		PandaRobot.MoveToPosition("Neutral")
		PandaRobot.MoveToPosition("AboveBoard")
		PandaRobot.MoveToPosition("Colunm1")
		PandaRobot.opengrip()
		PandaRobot.MoveToPosition("Neutral")
	
