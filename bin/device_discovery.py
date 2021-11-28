#!/usr/bin/python3
"""
	Description: Responsible for discovering device information
"""
import sys
import importlib
import json
from os.path import exists

# if settings file does not exist exit
if not exists(sys.argv[1]):
	print("Settings file not found: %s" %(sys.argv[1]))
	exit()

# Load settings and config
## settings
with open(sys.argv[1], 'r') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)

## Device registry
with open("%s/provider_registry.json" %(settings['cfg_dir']), 'r') as provider_registry_file:
	provider_registry_json = provider_registry_file.read()
provider_registry = json.loads(provider_registry_json)

## lights file
with open("%s/lights.json" %(settings['cfg_dir']), 'r') as lights_file:
	lights_json = lights_file.read()
light_properties = json.loads(lights_json)

# Discover Lights
for provider in provider_registry['light_providers']:
	try:
		module = importlib.import_module(provider)
	except ImportError:
		print('dude')
	for light_type in provider_registry['light_providers'][provider]:
		light = getattr(module, light_type)(settings)
		light.discover(light_properties)

## Save lights
with open("%s/lights.json" %(settings['cfg_dir']), 'w') as lights_file:
	json.dump(light_properties, lights_file)