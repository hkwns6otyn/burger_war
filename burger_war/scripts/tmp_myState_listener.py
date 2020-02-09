#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import tf
from nav_msgs.msg import Odometry
from tf2_msgs.msg import TFMessage
import tmp_targetsMap

class MyStateBot(object):
    def __init__(self, mySide = 'r'):
        self.mySide = mySide
        self.map = tmp_targetsMap.getTargetsMap()
        # self.odom_sub = rospy.Subscriber('odom', Odometry, self.odomCallback)

    def strategy(self):        
        r = rospy.Rate(10.0)
        tf_listener = tf.TransformListener()

        while not rospy.is_shutdown():
            try:                
                (trans,rot) = tf_listener.lookupTransform('map','base_footprint',rospy.Time(0))
                # (trans,rot) = tf_listener.lookupTransform('odom','base_footprint',rospy.Time(0))
                self.pose_x = trans[0]
                self.pose_y = trans[1]
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                # rospy.logerr("Failed to gettransform")
                continue
            # print(trans[0],trans[1])
            print(tmp_targetsMap.getNearestTarget(self.map,self.pose_x,self.pose_y))    

            r.sleep()

    # def odomCallback(self, data):
    #     # self.pose_x = data.pose.pose.position.x
    #     # self.pose_y = data.pose.pose.position.y          
    #     # print(self.pose_x, self.pose_y)
    #     print("")
    #     # print(tmp_targetsMap.getNearestTarget(self.map,self.pose_x,self.pose_y))


if __name__ == '__main__':    
    mySide = rospy.get_param("side", default="b")        
    rospy.init_node('my_state')
    bot = MyStateBot(mySide = mySide)
    bot.strategy()