#!/usr/bin/bash
# A very poor script to start mongo for test purposes

cd ~/mongo/
# Start
nohup mongod --config ~/Projects/pal_py_elements/tests/cfg/pal_mongodb.conf

# Stop
#pkill -9 mongod

# reset
#rm -Rf tests/data/mongodb/*