#!/usr/bin/env python
# -*- coding: utf-8 -*-

# respect judge/visualizeConsole.py
# respect all_sensor_sample.py

import rospy
from burger_war.msg import war_state

import requests
from time import sleep
import json

class WarStateBot(object):
    def __init__(self, mySide="r", displayLog = False):
        self.displayLog = displayLog
        self.state = war_state()
        self.war_state_pub = rospy.Publisher('war_state',war_state,queue_size=1)
    def fetchWarState(self):        
        resp = requests.get("http://localhost:5000/warState")        
        resp_json = resp.json()
        self.state.time = resp_json['time']        
        self.state.my_point = resp_json['scores'][mySide]
        if mySide == 'r':
            self.state.enemy_point = resp_json['scores']['b']        
        else:
            self.state.enemy_point = resp_json['scores']['r']        

    def strategy(self):        
        r = rospy.Rate(1)
        while not rospy.is_shutdown():
            # fetch war_state
            self.fetchWarState()
            if self.displayLog:                
                rospy.loginfo(self.state.time)
                rospy.loginfo(self.state.my_point-self.state.enemy_point)
                        
            # publish war_state topic
            self.war_state_pub.publish(self.state)

            r.sleep()

if __name__ == '__main__':
    rospy.init_node('war_state')    
    bot = WarStateBot(displayLog=True)    
    bot.strategy()