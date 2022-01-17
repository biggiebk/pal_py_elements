#!/usr/bin/python3
"""
Description: Run light tests
"""
import pytest
import json
import time
from pymongo import MongoClient
from lights.providers.pal_magic_hue import PalMagicHue

# Load settings
with open('cfg/test/settings.json', 'r') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)

# Run discovery Tests
discovery_args = [(settings)]

@pytest.mark.parametrize("settings", discovery_args)
def test_magic_hue_discover(settings):
	"""Test discover for magic hue lights"""
	magic_hue = PalMagicHue(settings)
	magic_hue.discover()
	assert magic_hue.get_device_by_name('office3')['address'] != ""

# Run light manipulation tests
pal_mongo = MongoClient(settings['database']['db_host'], settings['database']['db_port'],
  username=settings['database']['ele_user'], password=settings['database']['ele_password'])
ele_db = pal_mongo[settings['database']['ele_db_name']]
light_devices = ele_db['devices']
## Turn on with full bright white
magic_hue_on = { "event_type": "control", "provider": "lights.providers.pal_magic_hue", "type":"PalMagicHue",	"name": "office3",
	"power": True,	"red": -1,	"green": -1,	"blue": -1,	"brightness": 255 }
## Adjust brightness to half
magic_hue_low = {	"event_type": "control", "provider": "lights.providers.pal_magic_hue", "type":"PalMagicHue",	"name": "office3",
	"power": True,	"red": -1,	"green": -1,	"blue": -1,	"brightness": 75 }
## Adjust color blue
magic_hue_blue = { "event_type": "control", "provider": "lights.providers.pal_magic_hue", "type":"PalMagicHue",	"name": "office3",
	"power": True,	"red": 0,	"green": 0,	"blue": 255,	"brightness": 255 }
## Turn off
magic_hue_off = { "event_type": "control", "provider": "lights.providers.pal_magic_hue", "type":"PalMagicHue",	"name": "office3",
	"power": False,	"red": 0,	"green": 0,	"blue": 0,	"brightness": 255 }
magic_hue_args = [
	(settings, magic_hue_on, 5),
	(settings, magic_hue_low, 5),
	(settings, magic_hue_blue, 5),
	(settings, magic_hue_off, 0)]
@pytest.mark.parametrize("settings,event,sleep_time", magic_hue_args)
def test_magic_hue_manipulation(settings, event, sleep_time):
	"""Test to manipulate magic hue lights"""
	device = light_devices.find_one({"name": "office3"})
	magic_hue = PalMagicHue(settings)
	# Power on
	assert magic_hue.set(event, device) == None
	# Allow for some time to see changes
	time.sleep(sleep_time)
