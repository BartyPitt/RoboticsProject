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


def moveto(x,y,z,roll,pitch,yaw):
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

def closegrip():
	gripper_msg.data = [0, 0]
	gripper_publisher.publish(gripper_msg)
	rospy.sleep(2)

def opengrip():
	gripper_msg.data = [0.05, 0.05]
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

	moveto(0.3,0.4,0.7,pi,0,pi/4) # Neutral position
	opengrip()
	moveto(0.3,0.4,0.15,pi,0,pi/4) # Move to disk
	closegrip()
	moveto(0.3,0.4,0.7,pi,0,pi/4) # Neutral position
	moveto(0.6,0,0.7,pi,0,pi/4) # Above board
	moveto(0.6,0,0.64,pi,0,pi/4) # Column
	opengrip()
	moveto(0.3,0.4,0.7,pi,0,pi/4) # Neutral position

