"""
Load and delete models on Gazebo
Modified from Baxter SDK example (https://sdk.rethinkrobotics.com/wiki/Home)

Last modified by : R Saputra 2020
Modified on 2 March 2020 by Medad Newman
"""

import rospy
import os
from gazebo_msgs.srv import (SpawnModel, DeleteModel,)
from geometry_msgs.msg import (PoseStamped, Pose, Point, Quaternion,)
import tf



# To read from whereever the git root folder is.
def find_vcs_root(test, dirs=(".git",), default=None):
    import os
    prev, test = None, os.path.abspath(test)
    while prev != test:
        if any(os.path.isdir(os.path.join(test, d)) for d in dirs):
            return test
        prev, test = test, os.path.abspath(os.path.join(test, os.pardir))
    return default


def load_gazebo_models(c4_pose=Pose(position=Point(x=-0.45, y=-0.685, z=-.35)),
                       c4_reference_frame="world"):
    test = tf.transformations.quaternion_from_euler(0, 0, 0)
    c4_pose.orientation.x = test[0]
    c4_pose.orientation.y = test[1]
    c4_pose.orientation.z = test[2]
    c4_pose.orientation.w = test[3]


    dirname = find_vcs_root(os.path.dirname(__file__))

    print(dirname)
    filename = os.path.join(dirname, 'Models/connect4/model.sdf')
    print(filename)
    # Load Connect 4 SDF
    table_xml = ''
    with open (filename, "r") as c4_file:
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
