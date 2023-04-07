#!/usr/bin/env python  
import roslib
#roslib.load_manifest('learning_tf')

import rospy
import tf

if __name__ == '__main__':
    rospy.init_node('laser_tf')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        br.sendTransform((0.18, 0.0, 0.42),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "laser_link",
                         "base_link")
        br.sendTransform((0.18, 0.0, 0.42),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "camera_base_link",
                         "base_link")
        rate.sleep()

