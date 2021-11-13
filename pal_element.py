"""
Description: Contains the Element parent class

"""

import json

class PalElement():
	"""
		Description: Parent class used by elements.
		Responsible for:
			1. Basic constructor for starting elements.
			2. Initiates Kafka cosumer
			3. Contains method to push to Kafka as producer
	"""

	def __init__(self, settings_file):
		"""
			Construct for elemental classes.
			Responsible for:
				1. Loading settings.
				2. Initate topic consumer
			Requires:
				settings_file - Path to the elementals setting file
		"""
		self.settings_file = settings_file
		self.settings = {}
		self.__load_settings()
		self.settings['settings_file'] = settings_file

	def reload(self):
		"""
			Reloads the element
				1. Reloads the configuration
		"""
		self.__load_settings()


	## Private methods, best not to overide anything beyond this point

	def __load_settings(self):
		"""
			Description: Parent class used by other elements.
			Responsible for:
				1. Loading settings
			Requires:
				settings_file - Path to the elementals setting file
		"""
		with open(self.settings_file, 'r') as settings:
			settings_json = settings.read()
		self.settings = json.loads(settings_json)
