"""
Description: Contains the Element parent class

"""

import json

class Pal_Element():
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
		self.settings = {}
		self.__load_settings(settings_file)


	## Private methods, best not to overide anything beyond this point

	def __load_settings(self, settings_file):
		"""
			Description: Parent class used by other elements.
			Responsible for:
				1. Loading settings
			Requires:
				settings_file - Path to the elementals setting file
		"""
		with open(settings_file, 'r') as settings:
			settings_json = settings.read()
		# parse file
		self.settings = json.loads(settings_json)
