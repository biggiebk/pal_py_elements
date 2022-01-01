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
	print(f"Settings file not found: {sys.argv[1]}")
	sys.exit()

# Load settings and config
## settings
with open(sys.argv[1], 'r', encoding='utf-8') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)

## Device registry
with open(f"{settings['cfg_dir']}/provider_registry.json", 'r',
	encoding='utf-8') as provider_registry_file:
	provider_registry_json = provider_registry_file.read()
provider_registry = json.loads(provider_registry_json)

## lights file
with open(f"{settings['cfg_dir']}/lights.json", 'r', encoding='utf-8') as lights_file:
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
with open(f"{settings['cfg_dir']}/lights.json", 'w', encoding='utf-8') as lights_file:
	json.dump(light_properties, lights_file)
