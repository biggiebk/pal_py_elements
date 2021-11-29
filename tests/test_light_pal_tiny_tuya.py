#!/usr/bin/python3
"""
Description: Run light tests
"""
import pytest
import json
import time
from lights.providers.pal_tiny_tuya import PalTinyTuya

# Setup Data
with open('tests/cfg/settings_test.json', 'r') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)

with open('tests/cfg/lights.json', 'r') as lights_file:
	lights_json = lights_file.read()
lights = json.loads(lights_json)


# Run discovery Tests
discovery_args = [(settings,lights)]

@pytest.mark.parametrize("settings,lights", discovery_args)
def test_magic_hue_discover(settings, lights):
	"""Test discover for magic hue lights"""
	tuya = PalTinyTuya(settings)
	tuya.discover(lights)
	assert lights['office2']['address'] != None

# Run light manipulation tests
### Turn on with full bright white
tuya_on = {	"provider": "lights.providers.pal_tiny_tuya", "type":"PalTinyTuya",	"name": "office2",
	"power": True,	"red": -1,	"green": -1,	"blue": -1,	"brightness": 1000 }
### Adjust brightness to half
tuya_low = {	"provider": "lights.providers.pal_tiny_tuya", "type":"PalTinyTuya",	"name": "office2",
	"power": True,	"red": -1,	"green": -1,	"blue": -1,	"brightness": 100 }
### Adjust color blue
tuya_red = {	"provider": "lights.providers.pal_tiny_tuya", "type":"PalTinyTuya",	"name": "office2",
	"power": True,	"red": 255,	"green": 0,	"blue": 0,	"brightness": 1000 }
## Turn off
tuya_off = {	"provider": "lights.providers.pal_tiny_tuya", "type":"PalTinyTuya",	"name": "office2",
	"power": False,	"red": 0,	"green": 0,	"blue": 0,	"brightness": 255 }
tuya_args = [
	(settings, lights, tuya_on, 5),
	(settings, lights, tuya_low, 5),
	(settings, lights, tuya_red, 5),
	(settings, lights, tuya_off, 0)]
@pytest.mark.parametrize("settings,lights,event,sleep_time", tuya_args)
def test_tiny_tuya_manipulation(settings, lights, event, sleep_time):
	"""Test to manipulate magic hue lights"""
	tuya = PalTinyTuya(settings)
	tuya.set_properties(lights['office2'])
	# Power on
	assert tuya.set_status(event) == None
	# Allow for some time to see changes
	time.sleep(sleep_time)
