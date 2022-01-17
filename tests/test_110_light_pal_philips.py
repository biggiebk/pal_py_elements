#!/usr/bin/python3
"""
Description: Run tests for philips lights
"""
import pytest
import json
import time
from pymongo import MongoClient
from lights.providers.pal_philips import PalPhilips

# Load settings
with open('cfg/test/settings.json', 'r') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)

# Run discovery Test
discovery_args = [(settings)]

@pytest.mark.parametrize("settings", discovery_args)
def test_philips_discover(settings):
	"""Test discover for philips lights"""
	philips = PalPhilips(settings)
	philips.discover()
	assert philips.get_device_by_name('office1')['address'] != None

# Run light manipulation tests
pal_mongo = MongoClient(settings['database']['db_host'], settings['database']['db_port'],
  username=settings['database']['ele_user'], password=settings['database']['ele_password'])
ele_db = pal_mongo[settings['database']['ele_db_name']]
light_devices = ele_db['devices']
## Adjust brightness to half
philips_low = { "event_type": "control", "provider": "lights.providers.pal_philips", "type":"PalPhilips", "name": "office1",
	"power": True, "red": 0,	"green": 0,	"blue": 0,	"brightness": 75 }
## Full birghtness
philips_on = { "event_type": "control", "provider": "lights.providers.pal_philips", "type":"PalPhilips", "name": "office1",
	"power": True,	"red": 0,	"green": 0,	"blue": 0,	"brightness": 254 }
## Turn off
philips_off = {	"event_type": "control", "provider": "lights.providers.pal_philips", "type":"PalPhilips", "name": "office1",
	"power": False,	"red": 0,	"green": 0,	"blue": 0,	"brightness": 254 }
philips_args = [
	(settings, philips_low, 5),
	(settings, philips_on, 5),
	(settings, philips_off, 0)]
@pytest.mark.parametrize("settings,event,sleep_time", philips_args)
def test_philips_manipulation(settings, event, sleep_time):
	"""Test to manipulate philips lights"""
	philips = PalPhilips(settings)
	device = light_devices.find_one({"name": "office1"})
	# Power on
	assert philips.set(event, device) == None
	# Allow for some time to see changes
	time.sleep(sleep_time)
