#!/bin/bash

# set judge server state "running"
bash judge/test_scripts/set_running.sh localhost:5000
# gnome-terminal -e "roslaunch burger_war burger_teleop.launch"
gnome-terminal -e "roslaunch burger_war enemy_teleop.launch"

# launch robot control node
roslaunch burger_war sim_robot_run_2.launch
