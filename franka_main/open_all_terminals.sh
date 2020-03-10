#gnome-terminal --tab --title="$title1" --command="bash -c 'roscore; $SHELL'" \
#               --tab --title="$title2" --command="bash -c 'sleep 5s;source devel/setup.bash;roslaunch franka_gazebo panda_arm_hand.launch; $SHELL'" \
#               --tab --title="$title3" --command="bash -c 'sleep 5s;roslaunch panda_moveit_config demo.launch rviz_tutorial:=true; $SHELL'"



#gnome-terminal --tab --title="$title1" --command="bash -c 'cd ; cd Franka_ws ; source /devel/setup.bash; roscore; $SHELL'" \
#               --tab --title="$title2" --command="bash -c 'sleep 5s;source devel/setup.bash;roslaunch franka_control franka_control.launch robot_ip:=192.168.0.88 load_gripper:=true; $SHELL'" \
#               --tab --title="$title3" --command="bash -c 'sleep 2s;roslaunch panda_moveit_config panda_moveit.launch controller:=position; $SHELL'"\
#               --tab --title="$title3" --command="bash -c 'sleep 2s;roslaunch panda_moveit_config moveit_rviz.launch; $SHELL'"\
#               --tab --title="$title3" --command="bash -c 'sleep 2s;python main.py; $SHELL'"



gnome-terminal --tab --title="$title1" --command="bash -c 'roscore; $SHELL'" \
               --tab --title="$title3" --command="bash -c 'sleep 5s; source devel/setup.bash;roslaunch franka_control franka_control.launch robot_ip:=192.168.0.88 load_gripper:=true; $SHELL'"\
               --tab --title="$title3" --command="bash -c 'sleep 5s;roslaunch panda_moveit_config panda_moveit.launch controller:=position; $SHELL'"\
               --tab --title="$title3" --command="bash -c 'sleep 10s; roslaunch panda_moveit_config moveit_rviz.launch; $SHELL'"\






