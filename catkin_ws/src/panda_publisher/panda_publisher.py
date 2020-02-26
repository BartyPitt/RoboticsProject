#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState


def callback(data):
    print 'get data'

    '''
    pub1 = rospy.Publisher('/franka/joint1_position_controller/command', Float64, queue_size=1)
    pub2 = rospy.Publisher('/franka/joint2_position_controller/command', Float64, queue_size=1)
    pub3 = rospy.Publisher('/franka/joint3_position_controller/command', Float64, queue_size=1)
    pub4 = rospy.Publisher('/franka/joint4_position_controller/command', Float64, queue_size=1)
    pub5 = rospy.Publisher('/franka/joint5_position_controller/command', Float64, queue_size=1)
    pub6 = rospy.Publisher('/franka/joint6_position_controller/command', Float64, queue_size=1)
    pub7 = rospy.Publisher('/franka/joint7_position_controller/command', Float64, queue_size=1)
    J1_pos = Float64()
    J2_pos = Float64()
    J3_pos = Float64()
    J4_pos = Float64()
    J5_pos = Float64()
    J6_pos = Float64()
    J7_pos = Float64()
    
    pos = data.position
    print pos
    
    J1_pos.data = pos[0]
    J2_pos.data = pos[1]
    J3_pos.data = pos[2]
    J4_pos.data = pos[3]
    J5_pos.data = pos[4]
    J6_pos.data = pos[5]
    J7_pos.data = pos[6]
    print J7_pos
    
    
    pub1.publish(0.9)
    pub2.publish(0.9)
    pub3.publish(0.9)
    pub4.publish(0.9)
    pub5.publish(0.9)
    pub6.publish(0.9)
    pub7.publish(0.9)

    '''
    pos = data.position
    publishers = [rospy.Publisher('/franka/joint{}_position_controller/command'.format(i), Float64, queue_size=1) for i in range(1, 8)]

    for i in range(7):
        publishers[i].publish(pos[i])
    print 'published'
    




def talker():
    
    rospy.init_node('talker', anonymous=False)
    rospy.Subscriber("/move_group/fake_controller_joint_states", JointState, callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
