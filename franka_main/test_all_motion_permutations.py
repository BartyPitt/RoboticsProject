'''
Pseudocode
'''

# Set up & initialise game

# LOOP 

    # Human (Player) move

    # Call OpenCV function 
        # Get camera view
        # Create virtual board
        # Compare with previous board state
        # Identify change (chosen column)
        # Output column

    # Input player move (column) into bot
    # Advance turn

    # Bot (Ro-Bot) move

    # Identify best move (column)
    # Place bot move in virtual board
    # Translate into co-ordinates (distance factor)

    # Call Motion Planning algorithm
        # Take in move co-ordinate
        # Motion plan calculated
        # Execute robot motion
        # WAIT for robot move to finish

    # Advance turn

# Game finished

'''
Code
'''

# Import required python files
import c4_bot_functions as botfunc
from c4_class import Connect4Robot

# Import libraries

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf
from time import sleep
from math import pi
from std_msgs.msg import String, Float64MultiArray, MultiArrayDimension, Float64
from moveit_commander.conversions import pose_to_list


import itertools as it
import subprocess
import random


# Set up Franka Robot
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('panda_demo', anonymous=True)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()


display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory,queue_size=20)

ros_setup_message = """
rosservice call /move_group/trajectory_execution/set_parameters "config:
  doubles:
    - {name: 'allowed_start_tolerance', value: 0.05}"
"""
subprocess.call(ros_setup_message, shell=True)

#rospy.sleep(2)


PandaRobot = Connect4Robot()
# Calibration positions
PandaRobot.closegrip()
PandaRobot.define_coordinates([0.3, 0.35, 0.3, pi,0,pi/4])

# Carry out calibration
#PandaRobot.Calibration()




PandaRobot.AddPosition("DiskCollection" ,[PandaRobot.x1,PandaRobot.y1 + 0.2 ,PandaRobot.z1 + 0.1,PandaRobot.roll1,PandaRobot.pitch1,PandaRobot.yaw1])
PandaRobot.AddPosition("AboveBoard" , [PandaRobot.x1,PandaRobot.y1,PandaRobot.z1,PandaRobot.roll1,PandaRobot.pitch1,PandaRobot.yaw1])
for i in range(1,7):
    PandaRobot.AddPosition(str(i) ,[PandaRobot.x1,PandaRobot.y1 - PandaRobot.interpolation(i),PandaRobot.z1,PandaRobot.roll1,PandaRobot.pitch1,PandaRobot.yaw1])


position_names = ["DiskCollection","AboveBoard","1","2","3","4","5","6"]



# # Get object frames
# p = geometry_msgs.msg.PoseStamped()
# p.header.frame_id = robot.get_planning_frame()
# p.pose.position.x = 0.153745
# p.pose.position.y = -0.301298
# p.pose.position.z = 0.
# p.pose.orientation.x =  0.6335811
# p.pose.orientation.y = 0
# p.pose.orientation.z = 0.6335811
# p.pose.orientation.w = 0.4440158
# scene.add_mesh("Connect4", p,"connect4.STL")


if __name__ == "__main__":

    # Execute motion sequence
    print("executing motion sequence")
    combis = list(it.permutations(position_names, 2))

    random.shuffle(combis)



    for i in combis:
        a,b = i
        print("Going from position '{0}' to position '{1}'".format(a,b))
        PandaRobot.MoveToPosition(a)
        #PandaRobot.opengrip()
        #PandaRobot.closegrip()
        PandaRobot.MoveToPosition(b)
        #PandaRobot.opengrip()
        #PandaRobot.closegrip()


