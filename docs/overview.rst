Overview
====================

In this project, we got the Franka Emika "Panda" robot to play a game of Connect 4 against a human. To do this, we implemented Computer Vision, a Minimax Game Algorithm, Motion Planning and Collision Detection.
We also carried out extensive simulations of the robot's motion using Gazebo for visualisation.

The different elements of the project were written in discrete python scripts, elements of which were than called and executed within a main file.

The flow chart below shows an overview of the steps that are executed in the main file.

.. figure:: _static/Algorithm_flowchart.png
    :align: center
    :figclass: align-center

Main File Breakdown
-------------------

Setup Functions
-------------------

The main file collates all the code that is split into separate files into one executable file. To do this effectively, we first need to import all of the required external functions, and all the necessary python libraries.

.. warning::

    Although this is a python script, it will NOT run in an IDE in Windows. Many of the functions and libraries imported are specific for the ROS environment, which needs to be run inside a Virtual Machine, or on a ROS (Linux) dual-boot.

.. code-block:: python

    # Import required python files
    import c4_bot_functions as botfunc
    import open_cv as vision
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
    from IO import bcolors
    from time import sleep
    from math import pi
    from std_msgs.msg import String, Float64MultiArray, MultiArrayDimension, Float64
    from moveit_commander.conversions import pose_to_list

We also included a number of tools to aid debugging. Due to the limited access to the physical robot, most of the testing was done in simulation. 
Although the code operation for each state is similar, there are some small differences in code required to make the simulation run (particularly effective operation of the grippers).
These differences are highlighted in the 'Robot Movement' section of the documentation, and this switch is used to toggle between the code blocks.

In addition to this, OpenCV took a long time to develop and test, so in the meantime we created a switch so that the rest of the code could be tested without relying on computer vision.

.. code-block:: python

    simulation_status = True
    visionworking = False

When everything has been imported, the Franka Emika robot needs to be set up and initialised. The following code shows the setup procedure for this robot.

..code-block::

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

    display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)

    # This command makes ros to change the 'allowed_start_tolerance' to 0.05. Prevents controller failure
    ros_setup_message = """
    rosservice call /move_group/trajectory_execution/set_parameters "config:
    doubles:
        - {name: 'allowed_start_tolerance', value: 0.05}"
    """
    subprocess.call(ros_setup_message, shell=True)

    PandaRobot = Connect4Robot()

After setup, we then needed to define all of the positions that the robot arm had to visit during calibration and gameplay. This allowed us to use simple function calls for each position later in the game loop section of the code.
The positions were as follows: left & right corners (calibration), columns 0-6 (gameplay), disc collection (resting position)

.. code-block:: python

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