#!/usr/bin/python3
"""
Description: Run tests for philips lights
"""
import pytest
import threading
import json
import time
from pal_element import PalElement
from lights.light_consumer import LightConsumer
from lights.providers.pal_philips import PalPhilips

# Load settings
with open('cfg/test/db_settings.json', 'r') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)

# Kafka settings
with open('tests/cfg/settings_lights_test.json', 'r') as kafka_settings_file:
	kafka_settings_json = kafka_settings_file.read()
kafka_settings = json.loads(kafka_settings_json)

# Start Light Element Consumer in Daemon thread
light_consumer = LightConsumer('tests/cfg/settings_lights_test.json')
# Start the consumer
thread = threading.Thread(target=light_consumer.listen, args=())
thread.setDaemon(True)
thread.start()
# Just give it a brief pause
time.sleep(1)

# Run discovery Test
discovery_args = [(settings)]

@pytest.mark.parametrize("settings", discovery_args)
def test_philips_discover(settings):
	"""Test discover for philips lights"""
	philips = PalPhilips(settings)
	philips.discover()
	assert philips.get_device_by_name('office1')['address'] != None

# Run light manipulation tests
## Adjust brightness to half
philips_low = { "event_type": "control", "provider": "lights.providers.pal_philips", "type":"PalPhilips", "name": "office1",
	"power": True, "red": 0, "green": 0, "blue": 0, "brightness": 75 }
## Full birghtness
philips_on = { "event_type": "control", "provider": "lights.providers.pal_philips", "type":"PalPhilips", "name": "office1",
	"power": True,	"red": 0, "green": 0, "blue": 0, "brightness": 254 }
## Turn off
philips_off = {	"event_type": "control", "provider": "lights.providers.pal_philips", "type":"PalPhilips","name": "office1",
	"power": False,	"red": 0, "green": 0, "blue": 0, "brightness": 254 }
philips_args = [
	(settings, philips_low, 5),
	(settings, philips_on, 5),
	(settings, philips_off, 5)]
@pytest.mark.parametrize("settings,event,sleep_time", philips_args)
def test_light_element(settings, event, sleep_time):
	light_producer = PalElement('tests/cfg/settings_lights_test.json')
	light_producer.send_txt(kafka_settings['listen_topic'], json.dumps(event))
	time.sleep(sleep_time)
