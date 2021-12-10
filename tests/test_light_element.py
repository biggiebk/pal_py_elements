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

# Setup Data
with open('tests/cfg/settings_test.json', 'r') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)

with open('tests/data/lights.json', 'r') as lights_file:
	lights_json = lights_file.read()
lights = json.loads(lights_json)

# Start Light Element Consumer in Daemon thread
element_consumer = LightConsumer('tests/cfg/settings_test.json')
# Start the consumer
thread = threading.Thread(target=element_consumer.listen, args=())
thread.setDaemon(True)
thread.start()
# Just give it a brief pause
time.sleep(1)

# Run discovery Test
discovery_args = [(settings,lights)]

@pytest.mark.parametrize("settings,lights", discovery_args)
def test_philips_discover(settings, lights):
	"""Test discover for philips lights"""
	philips = PalPhilips(settings)
	philips.discover(lights)
	assert lights['office1']['address'] != None


# Run light manipulation tests
## Turn on with full birghtness
philips_on = { "event_type": "control", "provider": "lights.providers.pal_philips", "type":"PalPhilips",	"name": "office1",
	"power": True,	"red": 0,	"green": 0,	"blue": 0,	"brightness": 254 }
## Adjust brightness to half
philips_low = { "event_type": "control", "provider": "lights.providers.pal_philips", "type":"PalPhilips", "name": "office1",
	"power": True, "red": 0,	"green": 0,	"blue": 0,	"brightness": 75 }
## Turn off
philips_off = {	"event_type": "control", "provider": "lights.providers.pal_philips", "type":"PalPhilips", "name": "office1",
	"power": False,	"red": 0,	"green": 0,	"blue": 0,	"brightness": 254 }
philips_args = [
	(settings, philips_low, 30),
	(settings, philips_on, 30),
	(settings, philips_off, 5)]
@pytest.mark.parametrize("settings,event,sleep_time", philips_args)
def test_light_element(settings, event, sleep_time):
	element_producer = PalElement('tests/cfg/settings_test.json')
	element_producer.send_txt(settings['listen_topic'], json.dumps(event))
	time.sleep(sleep_time)
