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
import subprocess
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf
from time import sleep
from math import pi
from std_msgs.msg import String, Float64MultiArray, MultiArrayDimension, Float64
from moveit_commander.conversions import pose_to_list

# Set up Franka Robot
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('panda_demo', anonymous=True)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()

display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory,queue_size=20)

# This command makes ros to change the 'allowed_start_tolerance' to 0.05. Prevents controller failure
ros_setup_message = """
rosservice call /move_group/trajectory_execution/set_parameters "config:
  doubles:
    - {name: 'allowed_start_tolerance', value: 0.05}"
"""
subprocess.call(ros_setup_message, shell=True)

rospy.sleep(2)

#rospy.sleep(2)

PandaRobot = Connect4Robot()
# Calibration positions
PandaRobot.closegrip()
PandaRobot.define_coordinates([0.3, 0.35, 0.3, pi,0,pi/4])

# Carry out calibration
PandaRobot.Calibration()


PandaRobot.AddPosition("DiskCollection" ,[PandaRobot.x1,PandaRobot.y1 + 0.2 ,PandaRobot.z1 + 0.1,PandaRobot.roll1,PandaRobot.pitch1,PandaRobot.yaw1])
PandaRobot.AddPosition("AboveBoard" , [PandaRobot.x1,PandaRobot.y1,PandaRobot.z1,PandaRobot.roll1,PandaRobot.pitch1,PandaRobot.yaw1])
for i in range(0,7):
    PandaRobot.AddPosition(str(i) ,[PandaRobot.x1,PandaRobot.y1 - PandaRobot.interpolation(i),PandaRobot.z1,PandaRobot.roll1,PandaRobot.pitch1,PandaRobot.yaw1])

position_names = ["DiskCollection","AboveBoard","0","1","2","3","4","5","6"]

'''
Barty check and uncomment collision detection
'''
# Get object frames
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

# rospy.sleep(3)

# Set static variables
PLAYER = 0
BOT = 1

PLAYER_PIECE = 1
BOT_PIECE = 2

# Initialise game
board = botfunc.create_board()
game_over = False
turn = 0 # Human goes first
visionworking = False

while not game_over:
    if turn == PLAYER:

        if visionworking == False:

            print("")
            print("")
            move = int(input("Human (Player 1) choose a column:"))

            if move in range(0,7):
                col = move
            else:
                move = int(input("Human (Player 1) choose a column:"))

        else:
            # get new grid state from most recent capture
            vision.GetPositions('updated_gridstate.jpg')
            # analyse new grid state and get co-ordinate of most recent move
            new_move = vision.get_row_and_col(coordinates)
            # take the column index from the co-ordinate list, and assign to col
            col = new_move[1]

        if botfunc.is_valid_location(board, col):
            row = botfunc.get_next_open_row(board, col)
            botfunc.drop_piece(board, row, col, PLAYER_PIECE)

            if botfunc.winning_move(board, PLAYER_PIECE):
                game_over = True
                print("Human Wins!")

            # Advance turn & alternate between Player 1 and 2
            turn += 1
            turn = turn % 2

    if turn == BOT and not game_over:

        # Ask Ro-Bot (Player 2) to pick the best move based on possible opponent future moves
        col, minimax_score = botfunc.minimax(board, 4, -9999999, 9999999, True) # A higher value takes longer to run
        print("Ro-Bot (Player 2) chose column: {0}".format(col))


        if botfunc.is_valid_location(board, col):
            row = botfunc.get_next_open_row(board, col)
            botfunc.drop_piece(board, row, col, BOT_PIECE)
            print("=============================================================")
            print("   0   1   2   3   4   5   6 ")
            print("")
            botfunc.print_board(board)
            print("=============================================================")
            print("Ro-Bot is currently dropping the piece. Please wait!")

            # Execute motion sequence
            PandaRobot.opengrip()
            PandaRobot.MoveToPosition("DiskCollection")
            PandaRobot.closegrip()
            PandaRobot.MoveToPosition("AboveBoard")
            PandaRobot.MoveToPosition(str(col))
            PandaRobot.opengrip()

            if botfunc.winning_move(board, BOT_PIECE):
                print("Ro-Bot Wins!")
                game_over = True

            # Advance turn & alternate between Player 1 and 2
            turn += 1
            turn = turn % 2

    # When game finishes, wait for 30 seconds
    if game_over:
        PandaRobot.MoveToPosition("DiskCollection")
        print('Game finished!')




