#!/usr/bin/python3
"""
Description: Run device discovery checks for lights
"""
import json
from lights.providers.pal_magic_hue import PalMagicHue
from lights.providers.pal_philips import PalPhilips
from lights.providers.pal_tiny_tuya import PalTinyTuya

def __load_lights():
	with open('tests/cfg/lights.json', 'r') as lights_file:
		lights_json = lights_file.read()
	return json.loads(lights_json)

def __load_settings():
	with open('tests/cfg/settings_test.json', 'r') as settings_file:
		settings_json = settings_file.read()
	return json.loads(settings_json)

def test_magic_hue():
	"""Test discover for magic hue lights"""
	magic_hue = PalMagicHue(__load_settings())
	lights = __load_lights()
	magic_hue.discover(lights)
	assert lights['office3']['address'] != None

def test_philips():
	"""Test discover for philips lights"""
	philips = PalPhilips(__load_settings())
	lights = __load_lights()
	philips.discover(lights)
	assert lights['office1']['address'] != None

def test_tiny_tuya():
	"""Test discover for tiny tuya lights"""
	tuya = PalTinyTuya(__load_settings())
	lights = __load_lights()
	tuya.discover(lights)
	assert lights['office2']['address'] != None
