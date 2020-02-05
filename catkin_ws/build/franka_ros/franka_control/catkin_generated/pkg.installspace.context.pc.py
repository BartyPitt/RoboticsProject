# generated from catkin/cmake/template/pkg.context.pc.in
CATKIN_PACKAGE_PREFIX = ""
PROJECT_PKG_CONFIG_INCLUDE_DIRS = "${prefix}/include;/opt/ros/melodic/include/libfranka".split(';') if "${prefix}/include;/opt/ros/melodic/include/libfranka" != "" else []
PROJECT_CATKIN_DEPENDS = "actionlib;controller_interface;franka_hw;franka_msgs;geometry_msgs;message_runtime;pluginlib;realtime_tools;roscpp;sensor_msgs;tf2_msgs".replace(';', ' ')
PKG_CONFIG_LIBRARIES_WITH_PREFIX = "-lfranka_state_controller;-lfranka_control_services;/opt/ros/melodic/lib/libfranka.so.0.7.1".split(';') if "-lfranka_state_controller;-lfranka_control_services;/opt/ros/melodic/lib/libfranka.so.0.7.1" != "" else []
PROJECT_NAME = "franka_control"
PROJECT_SPACE_DIR = "/home/medad/RoboticsProject/catkin_ws/install"
PROJECT_VERSION = "0.7.0"
