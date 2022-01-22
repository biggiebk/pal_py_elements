"""
Description: Module containing the config preset classes
"""

import json
from pymongo import MongoClient
from beartype import beartype
from pal_element import PalElement

class ConfigEvent():
	"""
		Description: Parent class for config events
		Responsible for:
			1. Establishes a standard construct
			2. Sets up shared methods
	"""

	@beartype
	def __init__(self, settings: dict[str, any], collection) -> None:
		"""Construct for the config event"""
		self.settings = settings
		self.pal_mongo = MongoClient(self.settings['database']['db_host'],
			self.settings['database']['db_port'], username=self.settings['database']['ele_user'],
			password=self.settings['database']['ele_password'])
		self.pal_db = self.pal_mongo[self.settings['database']['ele_db_name']]
		self.pal_collection = self.pal_db[collection]
		self.params = None

	@beartype
	def trigger(self, params: dict[str, any]) -> None:
		"""Create, Update, delete, or get presets"""
		self.params = params
		if self.params['action'] == 'create':
			self.create()
		elif self.params['action'] == 'delete':
			self.delete()
		elif self.params['action'] == 'get':
			self.get()
		elif self.params['action'] == 'update':
			self.update()
		else:
			self._return_error(f"{self.params['action']}: is an unknown preset action for " +
				 f"{self.params['element']} element.")

	@beartype
	def create(self):
		"""Create a preset configuration"""
		self.pal_collection.insert_one(self.params['settings'])

	@beartype
	def delete(self):
		"""Delete a preset configuration"""
		preset = {'name': self.params['name']}
		self.pal_collection.delete_one(preset)

	@beartype
	def get(self):
		"""Get preset configurations"""
		if 'name' in self.params:
			find_preset = {'name': self.params['name']}
			result = self.pal_collection.find_one(find_preset)
			result.pop('_id')
			self._return_response([result])
		else: # Return them all
			results = []
			# This part does not feel very python like
			for record in self.pal_collection.find():
				record.pop('_id')
				results.append(record)
			self._return_response(results)

	@beartype
	def update(self):
		"""Update a preset configuration"""
		update = {'$set': self.params['settings']}
		self.pal_collection.update_one({'name': self.params['settings']['name']}, update)

## Private methods

	@beartype
	def _return_error(self, error_text: str) -> None:
		"""returns error to main debug channel"""
		error = {}
		error['session'] = self.params['session']
		error['tracking_id'] = self.params['tracking_id']
		error['error_text'] = error_text
		text = json.dumps(error)
		producer = PalElement(self.settings['settings_file'])
		producer.send_txt(self.settings['debug_topic'], text)
		producer.send_txt(self.params['return_topic'], text)

	@beartype
	def _return_response(self, value: list[dict[str, any]]) -> None:
		"""returns error to main debug channel"""
		response = {}
		response['session'] = self.params['session']
		response['tracking_id'] = self.params['tracking_id']
		response['response'] = value
		producer = PalElement(self.settings['settings_file'])
		producer.send_txt(self.params['return_topic'], json.dumps(response))
