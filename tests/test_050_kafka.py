#!/usr/bin/python3
"""
Description: Confirm the ability to communicate with Kafka as a consumer and producer
"""
# !!! - This test assumes kafka is already running - !!!
import time
import pytest
import json
import threading
from pal_element import PalElement
from support.initialize import InitializeElementsKafka

# !!! - This test assumes kafka is already running - !!!

# Ensure things are reset
initialize_element_kafka = InitializeElementsKafka('test')
initialize_element_kafka.reset()

# sleep for a bit
time.sleep(10)

# Lets initialize kafka
initialize_element_kafka.initialize()

## Start the tests

def kafka_event():
	"""
		function to enable testing of both the producer and consumer in elements
	"""
	kafka_consumer = PalElement('tests/cfg/settings_kafka_test.json')
	# Start the consumer
	thread = threading.Thread(target=kafka_consumer.listen, args=())
	thread.setDaemon(True)
	thread.start()
	time.sleep(1)
	kafka_producer = PalElement('tests/cfg/settings_kafka_test.json')
	kafka_producer.send_txt("TestTopic","I see you")
	time.sleep(1)

def test_kafka(capsys):
	"""Calls the Kafaka event"""
	kafka_event()
	captured = capsys.readouterr()
	assert captured.out == "TestTopic - I see you\n"

with open('cfg/test/kafka_settings.json', 'r') as kafka_file:
	kafka_json = kafka_file.read()
kafka = json.loads(kafka_json)
@pytest.mark.parametrize("topic", kafka['topics'])
def test_topics_exist(topic):
	existing_topics = initialize_element_kafka.get_topics()
	assert kafka['topics'][topic] in existing_topics
