#!/usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf
from time import sleep
from math import pi
from copy import deepcopy
from std_msgs.msg import String, Float64MultiArray, MultiArrayDimension, Float64
from moveit_commander.conversions import pose_to_list



class Connect4Robot():

	def __init__(self,GripperSizeExtended = 0.03 , GripperSizeRetracted = 0): #defult positions added to maintain compability with legacy code
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
		self.CartesianPath(Cordinates)

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

		group.set_pose_target(pose_goal) # Set new pose objective
		plan = group.go(wait=True) # Move to new pose
		rospy.sleep(2)
		# It is always good to clear your targets after planning with poses.
		group.clear_pose_targets()

	def movejoints(self, jointAngles):
		'''Takes in joint angles and moves to that pose'''
		joint_goal = group.get_current_joint_values()
		joint_goal = jointAngles
		group.go(joint_goal, wait=True)
		group.stop()

	def CartesianPath(self, Endposition , StartPosition = None):
		
		if StartPosition:
			StartPosition = self.CordinatesToPose(StartPosition)
		else:
			StartPosition = group.get_current_pose().pose
		
		Endposition = self.CordinatesToPose(Endposition)
		
		waypoints = []
		# start with the current pose
		waypoints.append(StartPosition)
		
		#TODO add in a level of path interpolation.
		
		waypoints.append(Endposition)
		
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

		group.execute(plan , wait = True)
		group.clear_pose_targets()
		return True
		



	def closegrip(self, simulation=True, GripOveride=None):
		if simulation:
			if GripOveride == None :
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




if __name__=="__main__":

	# Setting-up processes


	PandaRobot = Connect4Robot()
	rospy.sleep(3)
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
	