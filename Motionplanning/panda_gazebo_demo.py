#!/usr/bin/env python
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

if __name__=="__main__":
	moveit_commander.roscpp_initialize(sys.argv)
	rospy.init_node('panda_demo', anonymous=True)
	robot = moveit_commander.RobotCommander()
	scene = moveit_commander.PlanningSceneInterface()
	group_name = "panda_arm"
	group = moveit_commander.MoveGroupCommander(group_name)

	planning_frame = group.get_planning_frame()
	print "============ Reference frame: %s" % planning_frame

	# We can also print the name of the end-effector link for this group:
	eef_link = group.get_end_effector_link()
	print ("============ End effector: %s" % eef_link)

	# We can get a list of all the groups in the robot:
	group_names = robot.get_group_names()
	print ("============ Robot Groups:", robot.get_group_names())

	# Sometimes for debugging it is useful to print the entire state of the
	# robot:
	print ("============ Printing robot state")
	print (robot.get_current_state())
	print ("")

	# We can get the joint values from the group and adjust some of the values:
	joint_goal = group.get_current_joint_values()
	joint_goal[0] = 0
	joint_goal[1] = -pi/4
	joint_goal[2] = 0
	joint_goal[3] = -pi/2
	joint_goal[4] = 0
	joint_goal[5] = pi/3
	joint_goal[6] = 0

	# The go command can be called with joint values, poses, or without any
	# parameters if you have already set the pose or joint target for the group
	group.go(joint_goal, wait=True)

	# Calling ``stop()`` ensures that there is no residual movement
	group.stop()
	
	waypoints = []

	wpose = group.get_current_pose().pose
	wpose.position.z -= 0.2  # First move down (z)
	wpose.position.y += 0.2  # and sideways (y)
	waypoints.append(copy.deepcopy(wpose))

	wpose.position.x += 0.1  # Second move forward/backwards in (x)
	waypoints.append(copy.deepcopy(wpose))

	wpose.position.y -= 0.1  # Third move sideways (y)
	waypoints.append(copy.deepcopy(wpose))

	# We want the Cartesian path to be interpolated at a resolution of 1 cm
	# which is why we will specify 0.01 as the eef_step in Cartesian
	# translation.  We will disable the jump threshold by setting it to 0.0 disabling:
	(plan, fraction) = group.compute_cartesian_path(
	                                   waypoints,   # waypoints to follow
	                                   0.01,        # eef_step
	                                   0.0)         # jump_threshold
	group.execute(plan, wait=True)
