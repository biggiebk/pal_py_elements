#!/usr/bin/python3
"""
	Description: Initialize mongod DB for Pal Elements
"""
import sys
import json
from os.path import exists
from pymongo import MongoClient

# if settings file does not exist exit
if not exists(sys.argv[1]):
	print("Settings file not found: %s" %(sys.argv[1]))
	exit()

# Load db connection settings
with open(sys.argv[1], 'r') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)


# Connect first time
client = MongoClient(settings['host'], settings['port'])

# create db
mydatabase = client[settings['db_name']]

# create user
mydatabase.create_collection('elements')

# create collects
