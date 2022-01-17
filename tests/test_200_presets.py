#!/usr/bin/python3
"""
Description: Run tests for philips lights
"""
import pytest
import threading
import json
import time
from kafka import KafkaConsumer
from orchestrators.pal_element_orchestrators import PalElementConfigOrchestrator
from pal_element import PalElement

class PresetListener(PalElement):
	
	def __init__(sef, settings_file):
		super().__init__(settings_file=settings_file)

	def listen(self, topic, responses):
		"""
			Description: Connects to Kafka and consumes a topic
			Responsible for:
				1. Connecting to Kafka and listening for events/messages
				2. Calls the process_event method
		"""
		self.consumer = KafkaConsumer(self.settings['kafka']['topics'][topic],
			bootstrap_servers=self.settings['kafka']['connection']['ip'] +
			f":{self.settings['kafka']['connection']['port']}")
		for msg in self.consumer:
			responses.append(msg.value.decode('utf-8'))

# Settings
with open('cfg/test/settings.json', 'r') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)

# Start preset consumer in Daemon thread
preset_consumer = PalElementConfigOrchestrator('cfg/test/settings.json')
# Start the consumer
thread = threading.Thread(target=preset_consumer.listen, args=(['elemental_config_orch']))
thread.setDaemon(True)
thread.start()
# Just give it a brief pause
time.sleep(1)
pal_light_producer = PalElement('cfg/test/settings.json')

# Start response listener
responses = []
ResponseListener = PresetListener('cfg/test/settings.json')
thread = threading.Thread(target=ResponseListener.listen, args=(['preset_test',responses]))
thread.setDaemon(True)
thread.start()

# Create new
new_preset = {"request_type": "preset", "action": "create", "element": "light",
	"return_topic": settings['kafka']['topics']['preset_test'], "session": "hello", "tracking_id": "0",
		"settings": {"name": "Test_Color", "power": True, "red": 0, "green": 255, "blue": 255,
			"brightness": 1.0 } }
pal_light_producer.send_txt(settings['kafka']['topics']['elemental_config_orch'], json.dumps(new_preset))
time.sleep(1)

# Initiate check for new
get_preset = {"request_type": "preset", "action": "get", "element": "light",
	"return_topic": settings['kafka']['topics']['preset_test'], "name": new_preset['settings']['name'], "session": "hello",
	"tracking_id": "1"}
pal_light_producer.send_txt(settings['kafka']['topics']['elemental_config_orch'], json.dumps(get_preset))
time.sleep(1)

# Update new
new_preset['action'] = 'update'
new_preset['settings']['red'] = 75
new_preset['tracking_id'] = "2"
pal_light_producer.send_txt(settings['kafka']['topics']['elemental_config_orch'], json.dumps(new_preset))
time.sleep(1)

# Initiate check for updated
get_preset = {"request_type": "preset", "action": "get", "element": "light", "tracking_id": "3",
	"return_topic": settings['kafka']['topics']['preset_test'], "name": new_preset['settings']['name'], "session": "hello"}
pal_light_producer.send_txt(settings['kafka']['topics']['elemental_config_orch'], json.dumps(get_preset))


# Get all values before delete
get_presets = {"request_type": "preset", "action": "get", "element": "light",
	"return_topic": settings['kafka']['topics']['preset_test'], "session": "hello", "tracking_id": "4"}
pal_light_producer.send_txt(settings['kafka']['topics']['elemental_config_orch'], json.dumps(get_presets))
time.sleep(5)

# Delete new
delete_preset = {"request_type": "preset", "action": "delete", "element": "light",
	"tracking_id": "5", "return_topic": settings['kafka']['topics']['preset_test'],
	"name": new_preset['settings']['name']}
pal_light_producer.send_txt(settings['kafka']['topics']['elemental_config_orch'], json.dumps(delete_preset))
time.sleep(1)

# Get all values after delete
get_presets = {"request_type": "preset", "action": "get", "element": "light",
	"return_topic": settings['kafka']['topics']['preset_test'], "session": "hello", "tracking_id": "6"}
pal_light_producer.send_txt(settings['kafka']['topics']['elemental_config_orch'], json.dumps(get_presets))
time.sleep(5)

# Check responses
def test_create_light_preset():
	for response in responses:
		item = json.loads(response)
		if item['tracking_id'] == "1":
			assert item['response'][0]['name'] == new_preset['settings']['name']

def test_update_light_preset():
	for response in responses:
		item = json.loads(response)
		if item['tracking_id'] == "3":
			assert item['response'][0]['red'] == new_preset['settings']['red']

def test_update_get_all_light_preset():
	for response in responses:
		item = json.loads(response)
		if item['tracking_id'] == "6":
			assert len(item['response']) > 0

def test_delete_light_preset():
	before = 0
	for response in responses:
		item = json.loads(response)
		if item['tracking_id'] == "4":
			before = len(item['response'])
		elif item['tracking_id'] == "6":
			assert len(item['response']) < before
