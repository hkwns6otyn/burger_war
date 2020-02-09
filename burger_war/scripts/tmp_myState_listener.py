#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import tf
from nav_msgs.msg import Odometry
from tf2_msgs.msg import TFMessage

class MyStateBot(object):
    def __init__(self, mySide = 'r'):
        self.mySide = mySide
        self.odom_sub = rospy.Subscriber('odom', Odometry, self.odomCallback)
        # self.map_sub = rospy.Subscriber('tf',TFMessage, self.mapCallback)        

    def strategy(self):        
        r = rospy.Rate(10.0)
        tf_listener = tf.TransformListener()

        while not rospy.is_shutdown():
            try:                
                (trans,rot) = tf_listener.lookupTransform('map','base_footprint',rospy.Time(0))
                # (trans,rot) = tf_listener.lookupTransform('odom','base_footprint',rospy.Time(0))
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                # rospy.logerr("Failed to gettransform")
                continue
            print(trans[0],trans[1])
            r.sleep()

    def odomCallback(self, data):
        self.pose_x = data.pose.pose.position.x
        self.pose_y = data.pose.pose.position.y
        # rospy.loginfo("odom pose_x: {}".format(self.pose_x))
        # rospy.loginfo("odom pose_y: {}".format(self.pose_y))

    # def mapCallback(self,data):
    #     print("")


if __name__ == '__main__':    
    mySide = rospy.get_param("side", default="b")        
    rospy.init_node('my_state')
    bot = MyStateBot(mySide = mySide)
    bot.strategy()