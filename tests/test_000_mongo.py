#!/usr/bin/python3
"""
Description: Test initialization of the element database
"""
import pytest
import subprocess
import json
from pymongo import MongoClient
from os.path import exists
from bin.support.initialize import InitializeElementsDB

# Ensure DB is reset/empty
subprocess.run(["bin/mongo.sh", "test", "reset"])
# Start
subprocess.run(["bin/mongo.sh", "test", "start"])

# Lets initialize the DB
initialize_element = InitializeElementsDB('test')
initialize_element.initialize()

## Start the tests

# Load the settings and connect
with open("cfg/test/db_settings.json", 'r') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)
pal_mongo = MongoClient(settings['host'], settings['port'],
  username=settings['admin_user'], password=settings['admin_password'])
pal_db = pal_mongo['admin']

def test_users():
	"""Confirm users have been created"""
	results = pal_db.command("usersInfo")
	# Should have two users
	assert len(results['users']) == 2

def test_database():
	"""Confirm database was created"""
	# Confirm database is there
	results = pal_mongo.list_database_names()
	assert settings['db_name'] in results

with open('cfg/init/collections.json', 'r') as collections_file:
	collections_json = collections_file.read()
collections = json.loads(collections_json)
@pytest.mark.parametrize("collection", collections)
def test_collections(collection):
	"""Confirm collections exist"""
	pal_db = pal_mongo[settings['db_name']]
	results = pal_db.list_collection_names()
	assert collection in results

# Confirm document imports are good
@pytest.mark.parametrize("collection", collections)
def test_collection_documents(collection):
	pal_db = pal_mongo[settings['db_name']]
	count = pal_db[collection].count_documents({})
	if exists("cfg/init/%s.json" %(collection)):
		with open("cfg/init/%s.json" %(collection), 'r') as import_file:
			import_json = import_file.read()
		imports = json.loads(import_json)
		assert count == len(imports)
	else: # If no import should be zero
		assert count == 0
