#!/usr/bin/python3
"""
	Description: Contains classes to initialize Pal Elements components
"""
import sys
import json
from os.path import exists
from pymongo import MongoClient
from beartype import beartype
from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic

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
	def initialize(self) -> None:
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
		with open('cfg/collections.json', 'r') as collections_file:
			collections_json = collections_file.read()
		collections = json.loads(collections_json)

		# load unique index info
		with open('cfg/unique_indexes.json', 'r') as unique_indexes_file:
			unique_indexes_json = unique_indexes_file.read()
		unique_indexes = json.loads(unique_indexes_json)

		print('Creating Collections')
		for collection in collections:
			print("  %s" %(collection))
			if exists("cfg/%s.schema.json" %(collection)):
				print("    Including schema")
				with open("cfg/%s.schema.json" %(collection), 'r') as schema_file:
					schema_json = schema_file.read()
				schema = json.loads(schema_json)
				self.pal_db.create_collection(collection, validator=schema)
			else:
				self.pal_db.create_collection(collection)
			if collection in unique_indexes:
				print("    Creating unique index on %s" %(unique_indexes[collection]))
				self.pal_db[collection].create_index(unique_indexes[collection], unique = True)
			if exists("cfg/%s.json" %(collection)):
				print("    Importing collection")
				self.__import_collection(collection, "cfg/%s.json" %(collection))
			if exists("cfg/%s/%s.json" %(self.environment, collection)):
				print("    Importing enviornment specific collection")
				self.__import_collection(collection, "cfg/%s/%s.json" %(self.environment, collection))

	def __import_collection(self, collection, file) -> None:
		"""Import collection"""
		# Load db connection settings
		with open(file, 'r') as collection_file:
			collection_json = collection_file.read()
		imports = json.loads(collection_json)
		collection = self.pal_db[collection]
		collection.insert_many(imports)

class InitializeElementsKafka():
	"""
		Description: Initializes Kafka for elements
		Responsible for:
			1. Creating topics
	"""
	@beartype
	def __init__(self, environment: str) -> None:
		"""
			Description: Contrstruct for initializing Kafka
			Responsible for:
				1. Confirm the kafka settings file exists
				2. Load settings
				3. Init other variables
		"""

		self.environment = environment

		# if settings file does not exist exit
		if not exists("cfg/%s/kafka_settings.json" %(self.environment)):
			print("Settings file not found: %s" %(sys.argv[1]))
			exit()

		# Load db connection settings
		print('Loading kafka settings')
		with open("cfg/%s/kafka_settings.json" %(self.environment), 'r') as settings_file:
			settings_json = settings_file.read()
		self.settings = json.loads(settings_json)

		self.admin_client = KafkaAdminClient(
			bootstrap_servers=f"{self.settings['connection']['ip']}" +
				f":{self.settings['connection']['port']}")


	@beartype
	def get_topics(self) -> set:
		"""
			Description: Resets Kafaka for elements
			Responsible for:
				1. retrieving a list of topics
		"""
		print('Getting topics')
		topics = []
		consumer = KafkaConsumer(bootstrap_servers=f"{self.settings['connection']['ip']}" +
			f":{self.settings['connection']['port']}")
		return consumer.topics()

	@beartype
	def initialize(self) -> None:
		"""
			Description: Initializes Kafaka for elements
			Responsible for:
				1. Creates topics
		"""

		topics = []
		print('Creating Topics')
		for topic in self.settings['topics']:
			print(f"  {self.settings['topics'][topic]}")
			topics.append(NewTopic(name=self.settings['topics'][topic], num_partitions=1, replication_factor=1))

		self.admin_client.create_topics(new_topics=topics, validate_only=False)

	@beartype
	def reset(self) -> None:
		"""
			Description: Resets Kafaka for elements
			Responsible for:
				1. Deletes topics
		"""
		topics = []
		print('Deleting Topics')
		for topic in self.settings['topics']:
			print(f"  {self.settings['topics'][topic]}")
			topics.append(self.settings['topics'][topic])

		self.admin_client.delete_topics(topics)
