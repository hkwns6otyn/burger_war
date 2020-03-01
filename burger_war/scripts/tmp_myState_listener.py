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
from actionlib_msgs.msg import GoalStatusArray
from burger_war.msg import CvRect
from geometry_msgs.msg import Twist
from jsk_rviz_plugins.msg import OverlayText

import actionlib
from actionlib_msgs.msg import *
# from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
# from math import pi


class MyStateBot(object):

    def __init__(self, mySide='r'):
        self.mySide = mySide
        self.map = tmp_targetsMap.getTargetsMap()
        self.goalPub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=5)
        self.myStatePub = rospy.Publisher('my_state', OverlayText, queue_size=5)
        self.warStateSub = rospy.Subscriber('/war_state', war_state, self.warStateCallback)
        self.navStateSub = rospy.Subscriber('/move_base/status', GoalStatusArray, self.navStateCallback)
        self.cvRectSub = rospy.Subscriber('/cv_rect', CvRect, self.cvRectSubCallback)
        self.twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1000)

        self.war_state = war_state()
        self.war_state.target_names = []
        self.war_state.target_owner = []
        self.war_state.target_point = []

        self.my_state_text = OverlayText()
        self.my_state_text.text = ""

        self.r = 10.0   # rospy frequency

        self.isFoundEnemy = False
        self.rectData = CvRect()

        # Parameters of PID controller
        self.Kp = 0.005
        self.Ki = 0.0
        self.Kd = 0.00005
        self.integral = 0.0
        self.error = 0.0
        self.error_pre = 0.0
        self.dt = 1.0/self.r
        self.target_001 = 320.0

        # Parameters of DIST
        self.threshold_r = 50.0      # threshold of red area width
        self.threshold_g = 30.0     # threshold of green area width

    def strategy(self):

        r = rospy.Rate(self.r)
        nearestTargetName = "ROBOT"
        tf_listener = tf.TransformListener()
        # tf.waitForTransform('map','base_footprint',rospy.Time(0), rospy.Duration(10.0))
        # tf_listener.waitForTransform('map','base_footprint',rospy.Time(), rospy.Duration(4.0))
        sleep(2)

        while not rospy.is_shutdown():
            try:
                # tf_listener.waitForTransform('map','base_footprint',rospy.Time.now(), rospy.Duration(4.0))
                (trans, rot) = tf_listener.lookupTransform('map', 'base_footprint', rospy.Time(0))
                self.pose_x = trans[0]
                self.pose_y = trans[1]
                nearestTargetName_pre = nearestTargetName
                target_pos = PoseStamped()
                nearestTargetName = tmp_targetsMap.getNearestTarget(dcopy(self.map), dcopy(self.pose_x), dcopy(self.pose_y), self.war_state)
                if self.isFoundEnemy:
                    nearestTargetName = "ROBOT"
                    self.my_state_text.text = "Current Target : ROBOT"
                elif nearestTargetName == "":
                    self.my_state_text.text = "All Targets are MINE !!!!!"
                else:
                    self.my_state_text.text = "Current Target : " + nearestTargetName
                    nearestTargetPos = dcopy(self.map[nearestTargetName])
                    target_pos = tmp_targetsMap.getGoal(nearestTargetPos, nearestTargetName)
                    target_pos.header.stamp = rospy.Time.now()

                self.my_state_text.text = self.my_state_text.text + "\n Rect R Area :" + str(self.rectData.rect_r.area) + "\t Width :" + str(self.rectData.rect_r.length[0])
                self.my_state_text.text = self.my_state_text.text + "\n Rect G Area :" + str(self.rectData.rect_g.area) + "\t Width :" + str(self.rectData.rect_g.length[0])
                self.my_state_text.text = self.my_state_text.text + "\n Rect B Area :" + str(self.rectData.rect_b.area) + "\t Width :" + str(self.rectData.rect_b.length[0])

                if nearestTargetName != nearestTargetName_pre:
                    self.goalPub.publish(target_pos)

                self.my_state_text.text = self.my_state_text.text + "\nis Enemy found :" + str(self.isFoundEnemy)
                self.myStatePub.publish(self.my_state_text)

            except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
                rospy.logerr("Failed to gettransform")
                continue
            r.sleep()

    def warStateCallback(self, data):
        self.war_state = data

    def navStateCallback(self, data):
        if len(data.status_list) > 0:
            # 状態が取得できた場合
            status = data.status_list[0]
            # rospy.logerr(status.status)
            # if status.status == 3:
            #     print("GOAL!!!!!")

    def cvRectSubCallback(self, data):
        self.rectData = data
        self.pubTwistWithPIDController()

    def pubTwistWithPIDController(self):
        enemy = self.rectData.rect_r
        enemy_target = self.rectData.rect_g

        isFoundEnemyTarget = enemy_target.center != (-1.0, -1.0)
        self.isFoundEnemy = isFoundEnemyTarget  # or (enemy.center != (-1.0, -1.0))
        twist = Twist()

        if isFoundEnemyTarget:
            self.error = self.target_001 - enemy_target.center[0]
            self.integral += self.error * self.dt
            twist.angular.z = self.Kp * self.error + self.Kd * (self.error - self.error_pre) / self.dt  # + self.Ki * self.integral
            self.twist_pub.publish(twist)
        # elif self.isFoundEnemy:
        #     self.error = self.target_001 - enemy.center[0]
        #     self.integral += self.error * self.dt
        #     twist.angular.z = self.Kp * self.error + self.Kd * (self.error - self.error_pre) / self.dt  # + self.Ki * self.integral
        #     self.twist_pub.publish(twist)
        else:
            self.error = 0.0
            self.error_pre = 0.0
            self.integral = 0.0
            self.angular_z_PID = 0.0


if __name__ == '__main__':
    mySide = rospy.get_param("side", default="b")
    rospy.init_node('my_state')
    bot = MyStateBot(mySide=mySide)
    bot.strategy()
