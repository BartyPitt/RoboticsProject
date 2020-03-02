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

# Import libraries|

import sys
import copy
import rospy
import subprocess
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
import tf
from IO import bcolors
from time import sleep
from math import pi
from std_msgs.msg import String, Float64MultiArray, MultiArrayDimension, Float64
from moveit_commander.conversions import pose_to_list


################################################################
# SWITCHES to change

# Set to true if we are going to use the code for simulation.
# Ideally we dont want code different between simulation
# and reality
simulation_status = True
visionworking = False

################################################################

# Set up Franka Robot
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('panda_demo', anonymous=True)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
rospy.sleep(2)

# Get object frames
p = geometry_msgs.msg.PoseStamped()
#p = PoseStamped()
p.header.frame_id = robot.get_planning_frame()
p.pose.position.x = 0.4
p.pose.position.y = -0.301298
p.pose.position.z = -0.2
p.pose.orientation.x =  0.0
p.pose.orientation.y = 0
p.pose.orientation.z = 0.0
p.pose.orientation.w = 0.4440158
#scene.add_mesh("Connect4", p,"connect4.STL")
scene.add_box("table", p, (0.5, 1.5, 0.6))
rospy.sleep(2)

display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory,
                                               queue_size=20)

# This command makes ros to change the 'allowed_start_tolerance' to 0.05. Prevents controller failure
ros_setup_message = """
rosservice call /move_group/trajectory_execution/set_parameters "config:
  doubles:
    - {name: 'allowed_start_tolerance', value: 0.05}"
"""
subprocess.call(ros_setup_message, shell=True)


PandaRobot = Connect4Robot()

# Calibration positions
PandaRobot.define_coordinates([0.3, 0.35, 0.3, pi, 0, pi / 4])

# Initialise the positions the robot has to visit
PandaRobot.AddPosition("DiskCollection",
                       [PandaRobot.x1,
                        PandaRobot.y1 + 0.2,
                        PandaRobot.z1 + 0.1,
                        PandaRobot.roll1,
                        PandaRobot.pitch1,
                        PandaRobot.yaw1])


PandaRobot.AddPosition("AboveBoard", [PandaRobot.x1,
                                      PandaRobot.y1,
                                      PandaRobot.z1,
                                      PandaRobot.roll1,
                                      PandaRobot.pitch1,
                                      PandaRobot.yaw1])
for i in range(0, 7):
    PandaRobot.AddPosition(str(i),
                           [PandaRobot.x1,
                            PandaRobot.y1 + PandaRobot.interpolation(i),
                            PandaRobot.z1,
                            PandaRobot.roll1,
                            PandaRobot.pitch1,
                            PandaRobot.yaw1])


PandaRobot.robot_init()

position_names = ["DiskCollection", "AboveBoard", "0", "1", "2", "3", "4", "5", "6","LeftCorner","RightCorner"]

'''
Barty check and uncomment collision detection. 
@Medad: this is how its done: https://answers.ros.org/question/209030/moveit-planningsceneinterface-addbox-not-showing-in-rviz/
'''


# Carry out calibration
raw_input("Press Enter to move to DiskCollection point...")
# PandaRobot.MoveToPosition("DiskCollection")
PandaRobot.neutral()
raw_input("Press Enter to open gripper...")
PandaRobot.opengrip(simulation =simulation_status)
raw_input("Press Enter to close gripper...")
PandaRobot.closegrip(simulation =simulation_status)
raw_input("Press Enter to move to left corner...")
PandaRobot.MoveToPosition("LeftCorner")
raw_input("Press Enter to continue to right corner...")
PandaRobot.MoveToPosition("RightCorner")
raw_input("Press Enter to continue to game...")

# rospy.sleep(3)

# Set static variables
PLAYER = 0
BOT = 1

PLAYER_PIECE = 1
BOT_PIECE = 2

# Initialise game
board = botfunc.create_board()
game_over = False
turn = 0  # Human goes first


while not game_over:
    if turn == PLAYER:

        if visionworking == False:

            print("")
            botfunc.pretty_print_board(board)
            print("")

            # Sanitise the input
            while True:
                try:
                    move = int(input("Human (Player 1) choose a column:"))
                except:
                    print("Sorry, I didn't understand that.")
                    continue

                if move not in range(0, 7):
                    print("Sorry you have keyed in a out of bounds column value")
                    continue
                else:
                    col = move
                    break


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
                botfunc.pretty_print_board(board)
                print("Human Wins!")

            # Advance turn & alternate between Player 1 and 2
            turn += 1
            turn = turn % 2

    if turn == BOT and not game_over:

        # Ask Ro-Bot (Player 2) to pick the best move based on possible opponent future moves
        col, minimax_score = botfunc.minimax(board, 4, -9999999, 9999999, True)  # A higher value takes longer to run
        print("Ro-Bot (Player 2) chose column: {0}".format(col))

        if botfunc.is_valid_location(board, col):
            row = botfunc.get_next_open_row(board, col)
            botfunc.drop_piece(board, row, col, BOT_PIECE)
            print("")
            #botfunc.print_board(board)
            botfunc.pretty_print_board(board)

            print("Ro-Bot is currently heading to disk collection point")
            # Execute motion sequence
            # PandaRobot.MoveToPosition("DiskCollection")
            PandaRobot.neutral()
            PandaRobot.opengrip(simulation =simulation_status)
            raw_input("Press Enter to close gripper...")

            PandaRobot.closegrip(simulation =simulation_status)

            print("Ro-Bot is currently dropping the piece. Please wait!")
            rospy.sleep(0.3)

            #PandaRobot.MoveToPosition("AboveBoard")
            PandaRobot.MoveToPosition(str(col))
            PandaRobot.opengrip(simulation =simulation_status)
            PandaRobot.closegrip(simulation =simulation_status)

            if botfunc.winning_move(board, BOT_PIECE):
                print("Ro-Bot Wins!")
                game_over = True

            # Advance turn & alternate between Player 1 and 2
            turn += 1
            turn = turn % 2

    # When game finishes, wait for 30 seconds
    if game_over:
        #PandaRobot.MoveToPosition("DiskCollection")
        PandaRobot.neutral()
        print('Game finished!')