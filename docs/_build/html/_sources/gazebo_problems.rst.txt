Running on Gazebo
===============================

*"Failing to plan is planning to fail"*

*- Alan Lakein*

Before testing our code on the real Panda robot, we ran it on on a digital simulation, to validate that it would function
as expected. This was incredibly helpful as using a physically moving robot with unknown risks / movements would be a major risk.

In theory simulation works well, but in practice there were many problems that were encountered by the team when attempting to perform simulations in Gazebo.

Arm experiencing vibration / 'jittering'
----------------------------------------
This was mostly likely due to the fact that the PID settings for the robot's joints were not well tuned. Therefore,
this was investigated alongside the Gazebo simulations.

The 'default' PID values for the robot arm can be configured in ``franka_gazebo/config/default.yaml`` within the
``franka_gazebo`` ROS package.

During the simulation, a convenient graphical interface with sliders can be utilised to finetune PID values, by
running the following in another terminal:
``rosrun rqt_reconfigure rqt_reconfigure``

Once the ``rqt_reconfigure`` window is open, the slider interfaces can be found within ``gazebo_ros_control/pid_gains``
in the menu on the left hand side.

.. figure:: _static/gazebo_pid_interface.png
    :align: center
    :figclass: align-center

In order to fix this issue we took a number of approaches. In the first case we simply let the robot run and visually tuned the PID values
using the ``rqt_reconfigure`` window. It soon became clear that this would be impractical for tuning all 7 joints.

We decided to take a more disciplined approach and tune each joint in isolation. For this process we worked from the end effector down to the robot
base. To start we locked all the joints bellow the joint in question and set the joints *PID* constants to zero. We would then send a joint signal in a characteristic square wave to visually
characterize the joint behavior to perturbations::

    def sq_wave(t):
        f = 0.5
        const = 2 * np.pi * f * t
        delta_angle = (4/np.pi) * (np.sin(const) + (1/3)*np.sin(3*const) + (1/5)*np.sin(5*const)+ (1/7)*np.sin(7*const))
        # delta_angle = np.sin(np.pi*f*t)
        return delta_angle


*P* would be increased until the joint had minimal overshoot and small oscillations. We would then add
sufficient *D* till the joint was critically damped. This worked for the first 2 joints but the maximum *P* constant in the
dynamic tuning window was limited and were not able to continue increasing *P* to a suitable level for the lower larger joints. The reason for requiring such a high *P* was most likely
due to modelling errors in the physical simulation


Ultimately we returned to the default values found in ``franka_gazebo`` package. Using these values as a starting point we added a small amount of
*I* gain because we noticed that the end effector had trouble converging on the commanded position. The resulting performance was sufficiently to accurate
build a 5 high wall.


Brick model friction issues
--------------------------------------
This was a major issue in simulations, as otherwise the Panda's gripper would fail to pick up a brick and carry it in
its grip effectively.

The solution was to edit the brick object file and change its parameters regarding surface friction.

The file could be located in the following filepath: ``~/.gazebo/models/Brick/model-1_4.sdf``

With the model file ``model-1_4.sdf``, the following were changed::

        <surface>
          <friction>
            <ode>
              <mu>100</mu>
              <mu2>50</mu2>
              <fdir1>0 0 1</fdir1>
              <slip1>0.0</slip1>
              <slip2>0.0</slip2>
            </ode>
          </friction>
          <contact>
            <ode>
              <kp>100000.000000</kp>
              <kd>10.00000</kd>
              <max_vel>2.000000</max_vel>
              <min_depth>0.0001</min_depth>
            </ode>
          </contact>
        </surface>

We increased ``<mu>`` and ``<mu2>`` parameters. These are the static friction co-efficients used by the physics engine.

We increased ``<kp>`` to increase the stiffness of the collision and increased ``<kd>`` to add dampening.

Perhaps most importantly we set ``<max_vel>`` to a value larger then 0, and ``<min_depth>`` to a reasonable value. All bodies in Gazebo are soft, so when they collide there is
always some penetration past the surface boundary line. This is motion is counteracted a spring force. ``<max_vel>`` is the maximum velocity that an object can reach as
a result of that spring force. In earlier testing when we had wrongly tuned this parameter to zero, bricks would sink through the floor and continuing to vibrate indefinitely
upon being dropped. This *unrealistic* value seems to break the physics engine.

The total sum of these improvements allowed the brick to be grasped more effectively, and were less likely to slip from Panda's
gripper.

Gripper Friction friction issues
--------------------------------------

Friction is a function of both surfaces in contact. Thus it wasn't enough to just fix the brick, we also needed to consider the gripper.

Before considering fiction, however, we first addressed the fact that the gripper didn't open wide enough to pick up the brick. We fixed this by editing the ``hand.xacro`` file in the
``franka_gazebo`` package. Here we increased the maximum joint limit to give the gripper a 0.12 m span::

      <limit effort="400" lower="-0.001" upper="0.06" velocity="0.1"/>

Knowing that friction is a function of normal force, we increased the maximum allowable effort here as well. Never the less, while the gripper could
now open wide enough to pick up the brick, there wasn't enough friction to hold on.

Specifically we noticed that the gripper seemed to lack torsional friction. When it picked up the brick directly around the center of mass, the brick would
stay in longer. However, when it pick it up at an offset it would quickly rotate out.

In order to fix this issue we changed the torsion friction parameters of the gripper. Again in the ``hand.xacro`` file we added the following code to
overwrite the default::

    <gazebo reference="${ns}_leftfinger">
      <mu1>100</mu1>
        <mu2>100</mu2>
        <kp>100000</kp>
        <!-- <fdir1>0 0 0</fdir1> -->
        <collision name="${ns}__leftfinger_collision">
      <surface>
        <friction>
          <torsional>
            <coefficient>100</coefficient>
            <use_patch_radius>true</use_patch_radius>
            <patch_radius>0.1</patch_radius>
            <surface_radius>0.1</surface_radius>


While extremely optimistic with the values we set for the torsional friction - after this change, the gripper was able to consistently pick up the brick.
These changes didn't necessary reflect reality, but we felt validated as we knew in practice the brick would not fall out of the gripper. This belief was
eventually confirmed when we ran our simulated robot on the real Franka Panda.



