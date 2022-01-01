#!/usr/bin/python3
"""
	Description: Contains classes to initialize Pal Elements components
"""
import sys
import json
from os.path import exists
from pymongo import MongoClient
from beartype import beartype

class InitializeElementsDB():
	"""
		Description: Initializes the database for elements
		Responsible for:
			1. Creating the admin user
			2. Creating the database
			3. Creating the read/write user
			4. Creating collections, schemas, and indexes
	"""
	@beartype
	def __init__(self, environment: str) -> None:
		"""
			Description: Contrstruct for initializing the database
			Responsible for:
				1. Confirm the db settings file exists
				2. Load settings
				3. Init other variables
		"""

		self.environment = environment

		# if settings file does not exist exit
		if not exists("cfg/%s/db_settings.json" %(self.environment)):
			print("Settings file not found: %s" %(sys.argv[1]))
			exit()

		# Load db connection settings
		print('Loading DB settings')
		with open("cfg/%s/db_settings.json" %(self.environment), 'r') as settings_file:
			settings_json = settings_file.read()
		self.settings = json.loads(settings_json)

		self.pal_mongo = None
		self.pal_db = None

	@beartype
	def initialize(self):
		"""
			Description: Initializes the database for elements
			Responsible for:
				1. Creating the admin user
				2. Creating the database
				3. Creating the read/write user
				4. Creating collections, schemas, and indexes
		"""
		print('Initial DB connection')
		self.pal_mongo = MongoClient(self.settings['host'], self.settings['port'])
		# create admin user
		print("Creating admin user: %s" %(self.settings['admin_user']))
		self.pal_db = self.pal_mongo['admin']
		self.pal_db.command("createUser", self.settings['admin_user'],
			pwd=self.settings['admin_password'], roles=[{'role': "userAdminAnyDatabase", 'db': "admin"},
			"readWriteAnyDatabase"])

		# disconnect and create pal element user
		print("Disconnecting")
		self.pal_db = None
		self.pal_mongo.close()
		print("Print connecting as %s" %(self.settings['admin_user']))
		self.pal_mongo = MongoClient(self.settings['host'], self.settings['port'],
		  username=self.settings['admin_user'], password=self.settings['admin_password'])
		self.pal_db = self.pal_mongo['admin']
		print("Creating read/write user: %s" %(self.settings['ele_user']))
		self.pal_db.command("createUser", self.settings['ele_user'], pwd=self.settings['ele_password'],
			roles=[{ 'role': "readWrite", 'db': "pal_elements" }])

		# disconnect, connect as elements user, and create collections
		print('Disconnecting')
		self.pal_db = None
		self.pal_mongo.close()
		print("Connecting as: %s" %(self.settings['ele_user']))
		pal_mongo = MongoClient(self.settings['host'], self.settings['port'],
		  username=self.settings['ele_user'], password=self.settings['ele_password'])
		print("Create DB: %s" %(self.settings['db_name']))
		self.pal_db = pal_mongo[self.settings['db_name']]

		# create collections and import data
		with open('cfg/init/collections.json', 'r') as collections_file:
			collections_json = collections_file.read()
		collections = json.loads(collections_json)

		# load unique index info
		with open('cfg/init/unique_indexes.json', 'r') as unique_indexes_file:
			unique_indexes_json = unique_indexes_file.read()
		unique_indexes = json.loads(unique_indexes_json)

		print('Creating Collections')
		for collection in collections:
			print("  %s" %(collection))
			if exists("cfg/init/%s.schema" %(collection)):
				print("    Including schema")
				with open("cfg/init/%s.schema" %(collection), 'r') as schema_file:
					schema_json = schema_file.read()
				schema = json.loads(schema_json)
				self.pal_db.create_collection(collection, validator=schema)
			else:
				self.pal_db.create_collection(collection)
			if collection in unique_indexes:
				print("    Creating unique index on %s" %(unique_indexes[collection]))
				self.pal_db[collection].create_index(unique_indexes[collection], unique = True)
			if exists("cfg/init/%s.json" %(collection)):
				print("    Importing collection")
				self.__import_collection(collection)

	def __import_collection(self, name):
		"""Import collection"""
		# Load db connection settings
		with open("cfg/init/%s.json" %(name), 'r') as collection_file:
			collection_json = collection_file.read()
		imports = json.loads(collection_json)
		collection = self.pal_db[name]
		collection.insert_many(imports)
