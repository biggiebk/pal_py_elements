#!/usr/bin/python3
"""
Description: Run light tests
"""
import pytest
import json
import time
from lights.providers.pal_magic_hue import PalMagicHue

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
	magic_hue = PalMagicHue(settings)
	magic_hue.discover(lights)
	assert lights['office3']['address'] != None

# Run light manipulation tests
### Turn on with full bright white
magic_hue_on = {	"provider": "lights.providers.pal_magic_hue", "type":"PalMagicHue",	"name": "office3",
	"power": True,	"red": -1,	"green": -1,	"blue": -1,	"brightness": 255 }
### Adjust brightness to half
magic_hue_low = {	"provider": "lights.providers.pal_magic_hue", "type":"PalMagicHue",	"name": "office3",
	"power": True,	"red": -1,	"green": -1,	"blue": -1,	"brightness": 75 }
### Adjust color blue
magic_hue_blue = {	"provider": "lights.providers.pal_magic_hue", "type":"PalMagicHue",	"name": "office3",
	"power": True,	"red": 0,	"green": 0,	"blue": 255,	"brightness": 255 }
## Turn off
magic_hue_off = {	"provider": "lights.providers.pal_magic_hue", "type":"PalMagicHue",	"name": "office3",
	"power": False,	"red": 0,	"green": 0,	"blue": 0,	"brightness": 255 }
magic_hue_args = [
	(settings, lights, magic_hue_on, 5),
	(settings, lights, magic_hue_low, 5),
	(settings, lights, magic_hue_blue, 5),
	(settings, lights, magic_hue_off, 0)]
@pytest.mark.parametrize("settings,lights,event,sleep_time", magic_hue_args)
def test_magic_hue_manipulation(settings, lights, event, sleep_time):
	"""Test to manipulate magic hue lights"""
	magic_hue = PalMagicHue(settings)
	magic_hue.set_properties(lights['office3'])
	# Power on
	assert magic_hue.set_status(event) == None
	# Allow for some time to see changes
	time.sleep(sleep_time)
