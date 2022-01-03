#!/usr/bin/python3
"""
Description: Run light tests
"""
import pytest
import json
import time
from pymongo import MongoClient
from lights.providers.pal_tiny_tuya import PalTinyTuya

# Load settings
with open('cfg/test/db_settings.json', 'r') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)

# Run discovery Tests
discovery_args = [(settings)]

@pytest.mark.parametrize("settings", discovery_args)
def test_magic_hue_discover(settings):
	"""Test discover for magic hue lights"""
	tuya = PalTinyTuya(settings)
	tuya.discover()
	assert tuya.get_device_by_name('office2')['address'] != None

# Run light manipulation tests
pal_mongo = MongoClient(settings['db_host'], settings['db_port'],
  username=settings['ele_user'], password=settings['ele_password'])
ele_db = pal_mongo[settings['ele_db_name']]
light_devices = ele_db['light_devices']
office2 = light_devices.find_one({"name": "office2"})
## Turn on with full bright white
tuya_on = { "event_type": "control", "provider": "lights.providers.pal_tiny_tuya", "type":"PalTinyTuya",	"name": "office2",
	"power": True,	"red": -1,	"green": -1,	"blue": -1,	"brightness": 1000 }
## Adjust brightness to half
tuya_low = { "event_type": "control", "provider": "lights.providers.pal_tiny_tuya", "type":"PalTinyTuya",	"name": "office2",
	"power": True,	"red": -1,	"green": -1,	"blue": -1,	"brightness": 100 }
## Adjust color blue
tuya_red = {"event_type": "control", "provider": "lights.providers.pal_tiny_tuya", "type":"PalTinyTuya",	"name": "office2",
	"power": True,	"red": 255,	"green": 0,	"blue": 0,	"brightness": 1000 }
## Turn off
tuya_off = {"event_type": "control", "provider": "lights.providers.pal_tiny_tuya", "type":"PalTinyTuya",	"name": "office2",
	"power": False,	"red": 0,	"green": 0,	"blue": 0,	"brightness": 255 }
tuya_args = [
	(settings, office2, tuya_on, 5),
	(settings, office2, tuya_low, 5),
	(settings, office2, tuya_red, 5),
	(settings, office2, tuya_off, 0)]
@pytest.mark.parametrize("settings,device,event,sleep_time", tuya_args)
def test_tiny_tuya_manipulation(settings, device, event, sleep_time):
	"""Test to manipulate magic hue lights"""
	tuya = PalTinyTuya(settings)
	# Power on
	assert tuya.set(event, device) == None
	# Allow for some time to see changes
	time.sleep(sleep_time)
