import math

import rospy
from geometry_msgs.msg import PoseStamped

def getTargetsMapOnGAZEBO():
    Targets = {
        "FriedShrimp_N":    [0.0,       +0.35/2.0],
        "FriedShrimp_S":    [0.0,       -0.35/2.0],
        "FriedShrimp_E":    [+0.35/2.0, 0.0],
        "FriedShrimp_W":    [-0.35/2.0, 0.0],        
        "Omelette_N":       [+0.53,     +0.53+0.15/2.0],
        "Omelette_S":       [+0.53,     +0.53-0.15/2.0],
        "Tomato_N":         [-0.53,     +0.53+0.15/2.0],
        "Tomato_S":         [-0.53,     +0.53-0.15/2.0],
        "OctopusWiener_N":  [+0.53,     -0.53+0.15/2.0],
        "OctopusWiener_S":  [+0.53,     -0.53-0.15/2.0],
        "Pudding_N":        [-0.53,     -0.53+0.15/2.0],
        "Pudding_S":        [-0.53,     -0.53-0.15/2.0],
    }
    return Targets

def getTargetsMap():    
    Targets = {
        "FriedShrimp_N":    [+0.35/2.0,         0.0],
        "FriedShrimp_S":    [-0.35/2.0,         0.0],        
        "FriedShrimp_E":    [0.0,               -0.35/2.0],
        "FriedShrimp_W":    [0.0,               +0.35/2.0],        
        "Omelette_N":       [+0.53+0.15/2.0,    -0.53],
        "Omelette_S":       [+0.53-0.15/2.0,    -0.53],
        "Tomato_N":         [+0.53+0.15/2.0,    +0.53],
        "Tomato_S":         [+0.53-0.15/2.0,    +0.53],
        "OctopusWiener_N":  [-0.53+0.15/2.0,    -0.53],
        "OctopusWiener_S":  [-0.53-0.15/2.0,    -0.53],
        "Pudding_N":        [-0.53+0.15/2.0,    +0.53],
        "Pudding_S":        [-0.53-0.15/2.0,    +0.53],        
    }
    return Targets

distance = 0.25  # magic parm of distance to the target

def getGoal(targetPos, targetName):
    goalPos = targetPos
    goalDire = [0.0,0.0,0.0,1.0]
    
    if targetName[-1] == "N":
        goalPos[0] = goalPos[0] + distance
        goalDire[2] = 1.0
        goalDire[3] = 0.0
    elif targetName[-1] == "S":
        goalPos[0] = goalPos[0] - distance
        goalDire[2] = 0.0
        goalDire[3] = 1.0
    elif targetName[-1] == "W":
        goalPos[1] = goalPos[1] + distance
        goalDire[2] = math.sin(-math.pi/4.0)
        goalDire[3] = math.cos(-math.pi/4.0)
    elif targetName[-1] == "E":
        goalPos[1] = goalPos[1] - distance
        goalDire[2] = math.sin(math.pi/4.0)
        goalDire[3] = math.cos(math.pi/4.0)
    elif targetName == "enemy":
        print("Target is ENEMY!!")        
    else:
        print("ERROR!!!")

    target_pos = PoseStamped()
    target_pos.header.frame_id = "map"
    target_pos.pose.position.x = goalPos[0]
    target_pos.pose.position.y = goalPos[1]
    target_pos.pose.orientation.z = goalDire[2]
    target_pos.pose.orientation.w = goalDire[3]

    return target_pos

def getNearestTarget(Targets, x, y):
    dist = 99.0    
    nearestTarget = "a"
    for key in Targets:        
        tmp = (Targets[key][0] - x) **2 + (Targets[key][1] - y) **2 
        if tmp < dist:            
            nearestTarget = key
            dist = tmp
    return nearestTarget

