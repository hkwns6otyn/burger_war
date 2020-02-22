rosservice call /gazebo/reset_simulation "{}"
bash judge/test_scripts/reset_server.sh localhost:5000
bash judge/test_scripts/init_single_play.sh judge/marker_set/sim.csv localhost:5000 you enemy