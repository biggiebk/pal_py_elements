#!/usr/bin/bash
# A very poor script to start kafka for test purposes

cd ~/kafka/

# Start Zookeeper
nohup bin/zookeeper-server-start.sh config/zookeeper.properties  > zookeeper.log 2> zookeeper.err&

sleep 10

# Start kafka
nohup bin/kafka-server-start.sh config/server.properties > kafka.log 2> kafka.err &

# Create Topic
#bin/kafka-topics.sh --create --bootstrap-server 127.0.0.1:9092 --replication-factor 1 --partitions 1 --topic TestTopic
#bin/kafka-topics.sh --create --bootstrap-server 127.0.0.1:9092 --replication-factor 1 --partitions 1 --topic AudioTopic
#bin/kafka-topics.sh --create --bootstrap-server 127.0.0.1:9092 --replication-factor 1 --partitions 1 --topic LightsTopic
# Start Producer
#bin/kafka-console-producer.sh --broker-list 127.0.0.1:9092 --topic TestTopic
# Start Consumer
#bin/kafka-console-consumer.sh --bootstrap-server 127.0.0.1:9092 --topic TestTopic
