#!/usr/bin/python3
"""
Description: Test initialization of the element database
"""
import pytest
import subprocess
import json
from pymongo import MongoClient
from os.path import exists
from support.initialize import InitializeElementsDB

# Ensure DB is reset/empty
subprocess.run(["./mongo.sh", "test", "reset"])
# Start
subprocess.run(["./mongo.sh", "test", "start"])

# Lets initialize the DB
initialize_element_db = InitializeElementsDB('test')
initialize_element_db.initialize()

## Start the tests
# Load the settings and connect
with open("cfg/test/settings.json", 'r') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)
pal_mongo = MongoClient(settings['database']['db_host'], settings['database']['db_port'],
  username=settings['database']['admin_user'], password=settings['database']['admin_password'])
pal_db = pal_mongo['admin']

def test_users():
	"""Confirm users have been created"""
	results = pal_db.command("usersInfo")
	# Should have two users
	assert len(results['users']) == 2

def test_database():
	"""Confirm database was created"""
	results = pal_mongo.list_database_names()
	assert settings['database']['ele_db_name'] in results

with open('cfg/collections.json', 'r') as collections_file:
	collections_json = collections_file.read()
collections = json.loads(collections_json)
@pytest.mark.parametrize("collection", collections)
def test_collections(collection):
	"""Confirm collections exist"""
	pal_db = pal_mongo[settings['database']['ele_db_name']]
	results = pal_db.list_collection_names()
	assert collection in results

@pytest.mark.parametrize("collection", collections)
def test_collection_documents(collection):
	"""Confirm successful import of documents"""
	pal_db = pal_mongo[settings['database']['ele_db_name']]
	count = pal_db[collection].count_documents({})
	imports = 0
	# Check for generic import
	if exists("cfg/%s.json" %(collection)):
		with open("cfg/%s.json" %(collection), 'r') as import_file:
			import_json = import_file.read()
		imports = len(json.loads(import_json))
	# Check for environment specific import
	if exists("cfg/test/%s.json" %(collection)):
		with open("cfg/test/%s.json" %(collection), 'r') as import_file:
			import_json = import_file.read()
		imports = imports + len(json.loads(import_json))

	assert count == imports
