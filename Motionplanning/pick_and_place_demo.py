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

if __name__=="__main__":
	moveit_commander.roscpp_initialize(sys.argv)
	rospy.init_node('panda_demo', anonymous=True)
	robot = moveit_commander.RobotCommander()
	scene = moveit_commander.PlanningSceneInterface()
	group_name = "panda_arm"
	group = moveit_commander.MoveGroupCommander(group_name)

	gripper_publisher = rospy.Publisher('/franka/gripper_position_controller/command', Float64MultiArray, queue_size=1)
	gripper_msg = Float64MultiArray()
	gripper_msg.layout.dim = [MultiArrayDimension('', 2, 1)]

	# Set initial pose
	roll = pi
	pitch = 0
	yaw = -pi/4
	quaternion = tf.transformations.quaternion_from_euler(roll, pitch, yaw)

	pose_goal = geometry_msgs.msg.Pose()
	pose_goal.orientation.x = quaternion[0]
	pose_goal.orientation.y = quaternion[1]
	pose_goal.orientation.z = quaternion[2]
	pose_goal.orientation.w = quaternion[3]
	pose_goal.position.x = 0.3
	pose_goal.position.y = 0.15
	pose_goal.position.z = 0.6

	group.set_pose_target(pose_goal)
	plan = group.go(wait=True)
	rospy.sleep(2)
	# It is always good to clear your targets after planning with poses.
	group.clear_pose_targets()

	# Open grippers and move down to brick
	gripper_msg.data = [0.05, 0.05]
	gripper_publisher.publish(gripper_msg)

	brick_pose = group.get_current_pose().pose
	brick_pose.position.z -= 0.05  # First move down (z)

	group.set_pose_target(brick_pose)
	plan = group.go(wait=True)
	rospy.sleep(2)
	# It is always good to clear your targets after planning with poses.
	group.clear_pose_targets()

	# Close grippers to pick brick
	gripper_msg.data = [0.03, 0.03]
	gripper_publisher.publish(gripper_msg)

	rospy.sleep(2)

	waypoints = []

	wpose = group.get_current_pose().pose
	wpose.position.z += 0.05  # First move up (z)
	waypoints.append(copy.deepcopy(wpose))

	wpose.position.x -= 0.1  # Second move forward/backwards in (x)
	waypoints.append(copy.deepcopy(wpose))

	wpose.position.y -= 0.3  # Third move sideways (y)
	waypoints.append(copy.deepcopy(wpose))

	wpose.position.x += 0.1  # Fourth move forward/backwards in (x)
	waypoints.append(copy.deepcopy(wpose))

	wpose.position.z -= 0.05  # Finally move down (z)
	waypoints.append(copy.deepcopy(wpose))

	(plan, fraction) = group.compute_cartesian_path(
	                                   waypoints,   # waypoints to follow
	                                   0.01,        # eef_step
	                                   0.0)         # jump_threshold
	group.execute(plan, wait=True)
	rospy.sleep(2)

	group.clear_pose_targets()

	# Open grippers to place brick
	gripper_msg.data = [0.05, 0.05]
	gripper_publisher.publish(gripper_msg)

	rospy.sleep(2)

	waypoints = []

	wpose = group.get_current_pose().pose
	wpose.position.z += 0.05  # First move up (z)
	waypoints.append(copy.deepcopy(wpose))

	wpose.position.x -= 0.1  # Second move forward/backwards in (x)
	waypoints.append(copy.deepcopy(wpose))

	wpose.position.y += 0.3  # Third move sideways (y)
	waypoints.append(copy.deepcopy(wpose))

	wpose.position.x += 0.1  # Fourth move forward/backwards in (x)
	waypoints.append(copy.deepcopy(wpose))

	(plan, fraction) = group.compute_cartesian_path(
	                                   waypoints,   # waypoints to follow
	                                   0.01,        # eef_step
	                                   0.0)         # jump_threshold
	group.execute(plan, wait=True)
	group.clear_pose_targets()
