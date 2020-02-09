#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import tf
from nav_msgs.msg import Odometry
from tf2_msgs.msg import TFMessage
import tmp_targetsMap
from copy import deepcopy as dcopy
from geometry_msgs.msg import PoseStamped
class MyStateBot(object):
    def __init__(self, mySide = 'r'):
        self.mySide = mySide
        self.map = tmp_targetsMap.getTargetsMap()        
        self.goalPub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=5)        
        self.cnt = 10
    def strategy(self):        
        r = rospy.Rate(10.0)
        tf_listener = tf.TransformListener()

        while not rospy.is_shutdown():
            try:                
                (trans,rot) = tf_listener.lookupTransform('map','base_footprint',rospy.Time(0))                
                self.pose_x = trans[0]
                self.pose_y = trans[1]

                nearestTargetName = tmp_targetsMap.getNearestTarget(dcopy(self.map),dcopy(self.pose_x),dcopy(self.pose_y))
                nearestTargetPos = dcopy(self.map[nearestTargetName])
                target_pos = tmp_targetsMap.getGoal(nearestTargetPos, nearestTargetName)                        
                target_pos.header.stamp = rospy.Time.now()
                # target_pos.header.seq = rospy.Time.now()                
                if self.cnt > 0:
                    self.goalPub.publish(target_pos)                          
                    self.cnt = self.cnt - 1
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                rospy.logerr("Failed to gettransform")
                continue            
            r.sleep()

if __name__ == '__main__':    
    mySide = rospy.get_param("side", default="b")        
    rospy.init_node('my_state')
    bot = MyStateBot(mySide = mySide)    
    bot.strategy()