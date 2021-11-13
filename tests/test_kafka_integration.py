#!/usr/bin/python3
"""
Description: Check API calls for the National  Weather Service
In order for tests to run need to make sure that PYTHONPATH contains the pal/lib dir
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
	element_consumer = PalElementConsumer('tests/settings_test.json')
	# Start the consumer
	thread = threading.Thread(target=element_consumer.listen, args=())
	thread.setDaemon(True)
	thread.start()
	time.sleep(1)
	element_producer = PalElementProducer('tests/settings_test.json')
	element_producer.send_txt("TestTopic","I see you")
	time.sleep(1)


def test_kafka(capsys):
	kafka_event()
	captured = capsys.readouterr()
	assert captured.out == "TestTopic - I see you\n"
