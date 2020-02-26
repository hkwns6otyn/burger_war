#!/bin/bash

# 1. set state end

############# How to use #########################
# Args {server IP(default localhost:5000)}

# {server IP} localhost:5000

########## setting #########################

SERVER_IP=$1
RED_PLAYER_NAME=$2
BLUE_PLAYER_NAME=$3
# ########### script ########################
# set state to "running"
echo "=================set state "running"======================"
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"state":"end"}' ${SERVER_IP}/warState/players


# ready
echo "=================set ready players======================"
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d "{\"name\":\"${RED_PLAYER_NAME}\", \"side\":\"r\", \"id\":\"0000\"}" ${SERVER_IP}/submits
curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d "{\"name\":\"${BLUE_PLAYER_NAME}\", \"side\":\"b\", \"id\":\"0000\"}" ${SERVER_IP}/submits

