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

def getNearestTarget(Targets, x, y):
    dist = 99.0    
    nearestTarget = "a"
    for key in Targets:        
        tmp = (Targets[key][0] - x) **2 + (Targets[key][1] - y) **2 
        if tmp < dist:            
            nearestTarget = key
            dist = tmp
    return nearestTarget

