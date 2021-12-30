#!/usr/bin/python3
"""
Description: Test initialization of the element database
"""
import time
import threading
from pal_element import PalElement

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
