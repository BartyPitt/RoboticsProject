#!/usr/bin/env python

from std_msgs.msg import String, Float64MultiArray, MultiArrayDimension, Float64
import rospy
import tf
import geometry_msgs.msg
import moveit_commander

class Connect4Robot():

	def __init__(self,GripperSizeExtended = 0.03 , GripperSizeRetracted = 0, group = moveit_commander.MoveGroupCommander("panda_arm")): #defult positions added to maintain compability with legacy code
		'''Sets up the Inital setup conditions for the robot.
		TODO add in more setup conditions when more are needed.
		'''
		self.GripperSizeRetracted = GripperSizeRetracted
		self.GripperSizeExtended = GripperSizeExtended
		self.group = group
		self.__positions__ = dict() #the __ does nothing , it just signifies that I dont want the user to be writting to the memory location directly.

	
	def AddPosition(self , PositionName , PositionCordinates):
		'''A setter funciton that sets up the positions for the robot to travel to'''
		self.__positions__[PositionName] = PositionCordinates

	def interpolation(self, column):
		ydistance = (self.y2-self.y1)/6 * (column-1)
		return self.y1 + ydistance


	def Calibration(self , LeftCorner,dx = 0 , dy = -0.468 , dz = 0):
		'''Defines top left corner or board (relative to robot) and moves to calibration points'''
		[x,y,z,roll,pitch,yaw] = LeftCorner 
		RightCorner = [x+dx,y+dy,z+dz,roll,pitch,yaw]
		self.__positions__["LeftCorner"] = LeftCorner
		self.__positions__["RightCorner"] = RightCorner
		[self.x1 ,self.y1 ,self.z1 ,self.roll1 ,self.pitch1 ,self.yaw1]    = LeftCorner
		[self.x2 , self.y2 , self.z2 , self.roll2 , self.pitch2, self.yaw2] = RightCorner
        
		print("Moved to first calibration point")
		self.moveto([self.x1,self.y1,self.z1,self.roll1,self.pitch1,self.yaw1])
		raw_input("Press Enter to continue to second calibration point...")
		self.moveto([self.x2,self.y2,self.z2,self.roll2,self.pitch2,self.yaw2])
		print("Moved to second calibration point")
		raw_input("Press Enter to continue to game...")	
	
	def MoveToPosition(self ,Position):
		'''Takes the name of the position and moves the robot to that position.'''
		Cordinates = self.__positions__[Position]
		self.moveto(Cordinates)

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
		#rospy.sleep(2)
		# It is always good to clear your targets after planning with poses.
		self.group.clear_pose_targets()

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

