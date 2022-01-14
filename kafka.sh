#!/usr/bin/bash
# A very poor script to start kafka for test purposes

# Set environment
environment=$1

case $2 in

  'start')
    echo -e "\nStarting"
		cd ~/kafka/
		# Start Zookeeper
		nohup bin/zookeeper-server-start.sh config/zookeeper.properties  > zookeeper.log 2> zookeeper.err&
		sleep 60
		# Start kafka
		nohup bin/kafka-server-start.sh config/server.properties > kafka.log 2> kafka.err &
  ;;

  'stop')
		cd ~/kafka/
    echo -e "\nStopping"
		# Stop kafka
		nohup bin/kafka-server-stop.sh config/server.properties > kafka.stop.log 2> kafka.stop.err &
		sleep 60
		# Stop Zookeeper
		nohup bin/zookeeper-server-stop.sh config/zookeeper.properties  > zookeeper.stop.log 2> zookeeper.stop.err&
  ;;

  'reset')
    ./init_elements_kafka.py reset $environment
  ;;

  'init')
    ./init_elements_kafka.py init $environment
  ;;

  'get')
    ./init_elements_kafka.py get $environment
  ;;

esac
