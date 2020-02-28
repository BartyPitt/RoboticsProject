gnome-terminal --tab --title="$title1" --command="bash -c 'roscore; $SHELL'" \
               --tab --title="$title3" --command="bash -c 'sleep 5s; source devel/setup.bash; rosrun gazebo_ros gazebo; $SHELL'"\
               --tab --title="$title3" --command="bash -c 'sleep 5s; source devel/setup.bash; roslaunch panda_moveit_config demo.launch rviz_tutorial:=true; $SHELL'"\
               --tab --title="$title3" --command="bash -c 'sleep 5s; cd src/panda_publisher; python panda_publisher.py; $SHELL'"\
               --tab --title="$title2" --command="bash -c 'sleep 10s; source devel/setup.bash; roslaunch franka_gazebo panda_arm_hand.launch; $SHELL'" 



