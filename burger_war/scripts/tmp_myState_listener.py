#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep 
import rospy
import tf
from nav_msgs.msg import Odometry
from tf2_msgs.msg import TFMessage
import tmp_targetsMap
from copy import deepcopy as dcopy
from geometry_msgs.msg import PoseStamped
from burger_war.msg import war_state

from jsk_rviz_plugins.msg import OverlayText

class MyStateBot(object):
    def __init__(self, mySide = 'r'):
        self.mySide = mySide
        self.map = tmp_targetsMap.getTargetsMap()        
        self.goalPub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=5)                
        self.myStatePub = rospy.Publisher('my_state',OverlayText,queue_size=5)
        self.warStateSub = rospy.Subscriber('/war_state', war_state, self.warStateCallback)

        # self.cnt = 10
        self.war_state = war_state()
        self.war_state.target_names = []
        self.war_state.target_owner = []
        self.war_state.target_point = []

        
        self.my_state_text = OverlayText()
        self.my_state_text.text = ""

    def strategy(self):     
        
        r = rospy.Rate(10.0)
        tf_listener = tf.TransformListener()
        nearestTargetName = None
        sleep(3)   
        while not rospy.is_shutdown():
            try:                
                (trans,rot) = tf_listener.lookupTransform('map','base_footprint',rospy.Time(0))                
                self.pose_x = trans[0]
                self.pose_y = trans[1]                
                nearestTargetName_pre = nearestTargetName
                nearestTargetName = tmp_targetsMap.getNearestTarget(dcopy(self.map),dcopy(self.pose_x),dcopy(self.pose_y),self.war_state)

                if nearestTargetName == "":
                    # target_pos = t
                    self.my_state_text.text = "All Targets are MINE !!!!!"
                else:
                    self.my_state_text.text = "Current Target : " + nearestTargetName
                    
                    nearestTargetPos = dcopy(self.map[nearestTargetName])                                    
                    target_pos = tmp_targetsMap.getGoal(nearestTargetPos, nearestTargetName)                        
                    target_pos.header.stamp = rospy.Time.now()
                    if nearestTargetName != nearestTargetName_pre:
                        self.goalPub.publish(target_pos)                                        
                self.myStatePub.publish(self.my_state_text)
            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                rospy.logerr("Failed to gettransform")
                continue            
            r.sleep()

    def warStateCallback(self,data):                
        self.war_state = data

if __name__ == '__main__':    
    mySide = rospy.get_param("side", default="b")        
    rospy.init_node('my_state')
    bot = MyStateBot(mySide = mySide)    
    bot.strategy()

