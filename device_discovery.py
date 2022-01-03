#!/usr/bin/python3
"""
	Description: Responsible for discovering device information
"""
import sys
import importlib
import json
from os.path import exists
from pymongo import MongoClient

# if settings file does not exist exit
if not exists(sys.argv[1]):
	print(f"Settings file not found: {sys.argv[1]}")
	sys.exit()

# Load settings and config
## settings
with open(sys.argv[1], 'r', encoding='utf-8') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)

## Get provider registry info
pal_mongo = MongoClient(settings['host'], settings['port'],
  username=settings['ele_user'], password=settings['ele_password'])
ele_db = pal_mongo[settings['ele_db_name']]
col_providers = devices = ele_db['providers']

# Discover Lights
for providers in col_providers.find():
	for provider in providers().keys():
		try:
			module = importlib.import_module(provider)
		except ImportError:
			print(f"Could no locate {provider}")
		for light_type in providers[provider]:
			light = getattr(module, light_type)(settings)
			light.discover()
