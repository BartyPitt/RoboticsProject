Simulating the robot
===============================

Before testing on the real robot, it is vital to test your code on a simulator. We use Gazebo to visulise the movement of the Panda Emika robot to see if it behaves properly. Form experience, IF and ONLY if it works in the simulation is there a REMOTE chance that your code will work on the actual robot. 

Word of advice: **Simulate, Simulate, Simulate**. Until everything works perfectly in the simulation.


Note that the actual Franka Emika robot costs several thousand Euros, and you will have a very limited time with the actual robot. You can save a lot of time by simulating everything on your computer. By simulating, you can potentially avoid getting the robot to do unexpected things. E.g spin around and smash into the wall behind. It would be a very expensive error.

Starting up your simulation
-----------------------------
Open five terminals, navigate to ``/catkin_ws`` and run the following commands in each:

Run Roscore, the master messaging core

.. code-block:: bash

    roscore



Open up Gazebo, the simulation software

.. code-block:: bash

    source devel/setup.bash
    rosrun gazebo_ros gazebo


Now open up Rviz, and open up the Movit motion planner plugin used for motion planning.

.. code-block:: bash

    source devel/setup.bash
    roslaunch panda_moveit_config demo.launch rviz_tutorial:=true

Now you need to activate motion planning using the Movit plugin. Add motion Motion Planning in the ``Add`` button. Then make sure ``Planning Scene Topic`` is set to ``/planning_scene`` . Also, set ``Planning Request`` to ``panda_arm`` . Under the ``Planning`` tab, make sure ``Use Cartesian Path`` is selected. You can set it up as shown in the image below.



.. figure:: _static/planning_scene.png
    :align: center
    :figclass: align-center


Run the ''panda_publisher.py'' utility that broadcasts movement of the joints and gripper such that gazebo knows that it has moved.

.. code-block:: bash

    cd src/panda_publisher
    python panda_publisher.py


Finally, spawn the robot arm in Gazebo.

.. code-block:: bash

    source devel/setup.bash
    roslaunch franka_gazebo panda_arm_hand.launch


Running Connect Four game code
--------------------------------

Now that we have the simulation setup, we can run the code to move the robot and play the Connect Four game. We need to return to the home directory, ``\RoboticsProject``, and open a new terminal. We then navigate to ``franka_main``, where our python script to move the robot and play the game is stored. In your terminal opened in ``\RoboticsProject``:

.. code-block:: bash

    cd Franka_ws
    python main.py
  


Now you should be able to see the game startup on your terminal. It will give your instructions to help you position the Connect Four board right under the robot's gripper. More instructions on playing the game will be in the next section

..
  TODO: add in a link to the next section
  TODO: Show how to add in the STL file of the connect four board into Gazebo so that we can see it. I involves setting the path manually in gazebo gui and then running a python script.


Simulation setup screencast
-------------------------------- 

For your reference, here is video showing the whole setup operation that will allow you to run a full simulation.

.. raw:: html

    <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
        <iframe src="https://drive.google.com/file/d/1zKt-nPKSKOXqZ7UHFkeTi5kBK8eA0pko/preview" width="640" height="480"></iframe>
    </div>

