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
from c4_bot_functions import *
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


# Set up Franka Robot
moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('panda_demo', anonymous=True)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()


display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',moveit_msgs.msg.DisplayTrajectory,queue_size=20)

rospy.sleep(2)


# Add positions and relative names
PandaRobot = Connect4Robot()
PandaRobot.AddPosition("Neutral" , [0.3, 0.4, 0.7, pi, 0, pi/4])
PandaRobot.AddPosition("DiskCollection" , [0.3, 0.4, 0.15, pi, 0, pi/4])
PandaRobot.AddPosition("AboveBoard" , [0.6, 0, 0.7, pi, 0, pi/4])
PandaRobot.AddPosition("1" , [0.624, 0.347, 0.65, pi,0,pi/4]) # Not the right numbers
PandaRobot.AddPosition("2" , [0.6, 0.269, 0.65, pi, 0, pi/4]) # Not the right numbers
PandaRobot.AddPosition("3" , [0.6, 0.191, 0.65, pi, 0, pi/4]) # Not the right numbers
PandaRobot.AddPosition("4" , [0.6, 0.113, 0.65, pi, 0, pi/4]) # Not the right numbers
PandaRobot.AddPosition("5" , [0.6, 0.035, 0.65, pi, 0, pi/4]) # Not the right numbers
PandaRobot.AddPosition("6" , [0.6, -0.043, 0.65, pi, 0, pi/4]) # Not the right numbers
PandaRobot.AddPosition("7" , [0.624, -0.118, 0.65, pi,0,pi/4]) # Not the right numbers

# Calibration positions
PandaRobot.closegrip()
PandaRobot.moveto(0.5, 0.347412681245, 0.65, pi,0,pi/4)
print('Now in the 1st calibration position')
sleep(2)
PandaRobot.moveto(0.5, -0.118074733645, 0.65, pi,0,pi/4)
print('Now in the 2nd calibration position')
sleep(2)



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

# rospy.sleep(3)

# Set static variables
PLAYER = 0
BOT = 1

PLAYER_PIECE = 1
BOT_PIECE = 2

# Initialise game
board = create_board()
game_over = False
turn = 0 # Human goes first

while not game_over:
    if turn == PLAYER:

        col = int(input("Human (Player 1) choose a column:"))
        
        '''
        OpenCV code to go here: compare 'seen' grid with current board state, and update board state
        
        col = OpenCV output
        '''

        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_PIECE)

            if winning_move(board, PLAYER_PIECE):
                game_over = True
                print("Human Wins!")

            # Advance turn & alternate between Player 1 and 2
            turn += 1
            turn = turn % 2

    if turn == BOT and not game_over:

        # Ask Ro-Bot (Player 2) to pick the best move based on possible opponent future moves
        col, minimax_score = minimax(board, 4, -9999999, 9999999, True) # A higher value takes longer to run


        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, BOT_PIECE)

            # Execute motion sequence
            PandaRobot.MoveToPosition("Neutral")
            PandaRobot.opengrip()
            PandaRobot.MoveToPosition("DiskCollection")
            PandaRobot.closegrip()
            PandaRobot.MoveToPosition("Neutral")
            PandaRobot.MoveToPosition("AboveBoard")
            PandaRobot.MoveToPosition(str(col-1))
            PandaRobot.opengrip()
            PandaRobot.MoveToPosition("Neutral")

            if winning_move(board, BOT_PIECE):
                game_over = True
                #print("Ro-Bot Wins!")

            # Advance turn & alternate between Player 1 and 2
            turn += 1
            turn = turn % 2

    # print_board(board)

    # When game finishes, wait for 30 seconds
    if game_over:
        print('Game finished!')
