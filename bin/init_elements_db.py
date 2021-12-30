#!/usr/bin/python3
"""
	Description: Initialize mongod DB for Pal Elements
"""
import sys
import json
from os.path import exists
from pymongo import MongoClient

def import_collection(name):
	"""Import collection"""
	# Load db connection settings
	with open("cfg/init/%s.json" %(name), 'r') as providers_file:
		providers_json = providers_file.read()
	imports = json.loads(providers_json)
	collection = pal_db[name]
	collection.insert_many(imports)

# if settings file does not exist exit
if not exists(sys.argv[1]):
	print("Settings file not found: %s" %(sys.argv[1]))
	exit()

# Load db connection settings
with open(sys.argv[1], 'r') as settings_file:
	settings_json = settings_file.read()
settings = json.loads(settings_json)


# Connect first time
pal_mongo = MongoClient(settings['host'], settings['port'])
# create admin user
pal_db = pal_mongo['admin']
pal_db.command("createUser", settings['admin_user'], pwd=settings['admin_password'], roles=[{ 'role': "userAdminAnyDatabase", 'db': "admin" }, "readWriteAnyDatabase" ] )

# disconnect, connect as admin, and create pal element user
pal_db = None
pal_mongo.close()
pal_mongo = MongoClient(settings['host'], settings['port'],
  username=settings['admin_user'], password=settings['admin_password'])
pal_db = pal_mongo['admin']
pal_db.command("createUser", settings['ele_user'], pwd=settings['ele_password'], roles=[{ 'role': "readWrite", 'db': "pal_elements" }])

# disconnect, connect as elements user, and create collections
pal_db = None
pal_mongo.close()
pal_mongo = MongoClient(settings['host'], settings['port'],
  username=settings['ele_user'], password=settings['ele_password'])
pal_db = pal_mongo[settings['db_name']]

# create collections and import data# Load db connection settings
with open('cfg/init/collections.json', 'r') as collections_file:
	collections_json = collections_file.read()
collections = json.loads(collections_json)

for collection in collections:
	pal_db.create_collection(collection)
	if exists("cfg/init/%s.json" %(collection)):
		import_collection(collection)
