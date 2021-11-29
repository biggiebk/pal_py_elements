#!/usr/bin/python3
"""
Description: Run tests for philips lights
"""
import pytest
import json
import time
from lights.providers.pal_philips import PalPhilips

# Setup Data
with open('tests/cfg/settings_test.json', 'r') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)

with open('tests/cfg/lights.json', 'r') as lights_file:
	lights_json = lights_file.read()
lights = json.loads(lights_json)


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
philips_on = {	"provider": "lights.providers.pal_philips", "type":"PalPhilips",	"name": "office1",
	"power": True,	"red": 0,	"green": 0,	"blue": 0,	"brightness": 254 }
## Adjust brightness to half
philips_low = {	"provider": "lights.providers.pal_philips", "type":"PalPhilips", "name": "office1",
	"power": True,	"red": 0,	"green": 0,	"blue": 0,	"brightness": 75 }
## Turn off
philips_off = {	"provider": "lights.providers.pal_philips", "type":"PalPhilips", "name": "office1",
	"power": False,	"red": 0,	"green": 0,	"blue": 0,	"brightness": 254 }
philips_args = [
	(settings, lights, philips_on, 5),
	(settings, lights, philips_low, 5),
	(settings, lights, philips_off, 0)]
@pytest.mark.parametrize("settings,lights,event,sleep_time", philips_args)
def test_philips_manipulation(settings, lights, event, sleep_time):
	"""Test to manipulate philips lights"""
	philips = PalPhilips(settings)
	philips.set_properties(lights['office1'])
	# Power on
	assert philips.set_status(event) == None
	# Allow for some time to see changes
	time.sleep(sleep_time)
