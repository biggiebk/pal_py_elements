#!/usr/bin/python3
"""
Description: Confirm the ability to communicate with Kafka as a consumer and producer
"""
import time
import threading
from pal_element_consumer import PalElementConsumer
from pal_element_producer import PalElementProducer

# content of test_sample.py
def kafka_event():
	"""
		function to enable testing of both the producer and consumer in elements
	"""
	element_consumer = PalElementConsumer('tests/cfg/settings_test.json')
	# Start the consumer
	thread = threading.Thread(target=element_consumer.listen, args=())
	thread.setDaemon(True)
	thread.start()
	time.sleep(1)
	element_producer = PalElementProducer('tests/cfg/settings_test.json')
	element_producer.send_txt("TestTopic","I see you")
	time.sleep(1)


def test_kafka(capsys):
	"""Calls the Kafaka event"""
	kafka_event()
	captured = capsys.readouterr()
	assert captured.out == "TestTopic - I see you\n"
