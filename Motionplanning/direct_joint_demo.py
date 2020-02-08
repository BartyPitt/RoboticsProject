#!/usr/bin/env python

import rospy
import math
from std_msgs.msg import Float64MultiArray, MultiArrayDimension, Float64


if __name__ == '__main__':
    rospy.init_node('example_joint_publisher')

    initial = [0, 0, 0, -0.5, 0, 0.5, 0.75]
    publishers = [rospy.Publisher('/franka/joint{}_position_controller/command'.format(i), Float64, queue_size=1) for i in range(1, 8)]
    gripper_publisher = rospy.Publisher('/franka/gripper_position_controller/command', Float64MultiArray, queue_size=1)
    gripper_msg = Float64MultiArray()
    gripper_msg.layout.dim = [MultiArrayDimension('', 2, 1)]

    rospy.sleep(5)
    rospy.loginfo("Setting initial pose.")
    for i in range(7):
        publishers[i].publish(initial[i])

    start = rospy.Time.now()

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        elapsed = rospy.Time.now() - start
        delta_angle = math.pi / 16 * (math.cos(math.pi / 5 * elapsed.to_sec()))
        gripper_msg.data = [0.05 * (1 + math.cos(math.pi / 5 * elapsed.to_sec()))/ 2,0.05 * (1 + math.cos(math.pi / 5 * elapsed.to_sec()))/ 2]	# right gripper position (m)
        for i in range(7):
            publishers[i].publish(initial[i] + delta_angle)					# joint angle (radians)
        gripper_publisher.publish(gripper_msg)
    rate.sleep()
