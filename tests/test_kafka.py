#!/usr/bin/python3
"""
Description: Check API calls for the National  Weather Service
In order for tests to run need to make sure that PYTHONPATH contains the pal/lib dir
"""
import time
import threading
from pal_element import Pal_Element

# content of test_sample.py
def kafka_event():
	"""
		function to enable testing of both the producer and consumer in elements
	"""
	element = Pal_Element('tests/element_test.json')
	# Start the consu
	thread = threading.Thread(target=element.consumer, args=())
	thread.setDaemon(True)
	thread.start()
	#element.consumer()
	time.sleep(1)
	element.producer("TestTopic","I see you")
	time.sleep(1)

def test_kafka(capsys):
	kafka_event()
	captured = capsys.readouterr()
	assert captured.out == "TestTopic - I see you\n"
