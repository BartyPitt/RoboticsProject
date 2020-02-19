"""
Load and delete models on Gazebo
Modified from Baxter SDK example (https://sdk.rethinkrobotics.com/wiki/Home)

Last modified by : R Saputra
2020
"""

import rospy

from gazebo_msgs.srv import (SpawnModel, DeleteModel,)
from geometry_msgs.msg import (PoseStamped, Pose, Point, Quaternion,)
import tf


def load_gazebo_models(c4_pose=Pose(position=Point(x=0.1, y=-0.35, z=-.3)),
                       c4_reference_frame="world"):
    test = tf.transformations.quaternion_from_euler(0, 0, 0)
    c4_pose.orientation.x = test[0]
    c4_pose.orientation.y = test[1]
    c4_pose.orientation.z = test[2]
    c4_pose.orientation.w = test[3]


    # Load Connect 4 SDF
    table_xml = ''
    with open ("/home/user/Desktop/RoboticsProject/Models/connect4/model.sdf", "r") as c4_file:
        c4_xml=c4_file.read().replace('\n', '')


    # Spawn Table SDF
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        spawn_sdf = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        resp_sdf = spawn_sdf("connect4", c4_xml, "/",
                             c4_pose, c4_reference_frame)
    except rospy.ServiceException, e:
        rospy.logerr("Spawn SDF service call failed: {0}".format(e))

def delete_gazebo_models():
    try:
        delete_model = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
        resp_delete = delete_model("connect4")
        # resp_delete = delete_model("block")
    except rospy.ServiceException, e:
        rospy.loginfo("Delete Model service call failed: {0}".format(e))

def main():
    """RSDK Inverse Kinematics Pick and Place Example"""
    rospy.init_node("load_gazebo_models")

    load_gazebo_models()
    # rospy.sleep(10.0)
    # delete_gazebo_models()

if __name__ == '__main__':
    main()