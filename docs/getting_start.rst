Getting Started
========================

In order to run the game script, you will have to install ROS and the simulation packages.

Set Up
-------------------------


Installing ROS
-------------------------
.. note::

    It is assumed that you do **not** have ROS installed on your Ubuntu OS. The code we use here is tested on ROS Melodic on Ubuntu 18.1 and the following instructions show the installation steps for ROS Melodic.

First, make sure your Debian package index is up-to-date:

.. code-block:: bash

    sudo apt update


It is recommened that you do the full ROS desktop installation that comes with: ROS, rqt, rviz, robot-generic libraries, 2D/3D simulators and 2D/3D perception


.. code-block:: bash

    sudo apt install ros-melodic-desktop-full

Now should have installed ROS Melodic on your computer as well as  Gazebo (for visualising simulations) and RVIZ (for setting up and visualising motion planning)

You will need to install catkin, the ROS build system.

.. code-block:: bash

	sudo apt-get install ros-melodic-catkin python-catkin-tools




Installing Movit
---------------------------------------
Movit is the motion planning Rviz plugin that can be interacted with in Rviz. To install the prebuilt binaries, type in to your terminal

.. code-block:: bash
	
	sudo apt install ros-melodic-moveit


Installing Project folders
-----------------------------

You would first clone the project repository into your home folder.

.. code-block:: bash

    git clone https://github.com/BartyPitt/RoboticsProject.git

Now you have to make sure the submodules are updated.

.. code-block:: bash

    cd RoboticsProject
    git submodule sync
    git submodule update --init --force --recursive


The submodules that you will be downloading are:

* franka_gazebo : Contains 3D models of robot, for collision detection and rendering.
* franka_ros : To use ROS to control the Franka Emika robot
* libfranka : Driver software to control the Franka Emika robot
* moveit_tutorials : Tutorial documentation files for using Movit motion planner(not really necessary)
* panda_moveit_config : Contains demos using Movit motion planner


Some of these submodules have been forked and customised for our particular Franka Emika Robot.

Compiling all necessary files
--------------------------------

You have pulled all the dependencies for gazebo, Rviz but now you need to compile them. Go to your catkin workspace.

.. code-block:: bash

    cd catkin_ws

Now you need to compile all the driver code. To do that, in your ``catkin_ws`` folder

.. code-block:: bash

    catkin_make

You will find that it takes a minute or two to build the driver files.

Now you should all be ready to run your simulation code.