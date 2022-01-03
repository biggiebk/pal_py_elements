"""
Description: Dynamicly calls the required light class to handle the requested event
"""

import importlib
import json
from beartype import beartype
from pal_element import PalElement

class Request():

	"""
		Description: Checks the request type and sends the request to the correct kafka element
		Responsible for:
			1. Parses the JSON
			1. Locates the provider/module and the type of light
			2. iniates the light
			3. Contains method to push to Kafka as producer
	"""
	@beartype
	def __init__(self, settings, event_dict: dict[str, any]) -> None:
		"""Contruct for the light event"""
		self.settings = settings
		self.event_dict = event_dict
		self.light_properties = self.get_light_properties()

	@beartype
	def trigger(self) -> None:
		'''
			Trigger method
			Responsible for:
				1. Locating the provider modules
				2. Initiating the requested light class
				3. If error send update back to return topic
		'''
		#Converter the provider name to a module
		module = importlib.import_module(self.light_properties['provider'])

		# Load the class
		try:
			light = getattr(module, self.light_properties['type'])(self.settings)
			light.set(self.event_dict, self.light_properties)
		except ModuleNotFoundError:
			self.__return_error("Unable to locate provider: %s" %(self.light_properties['provider']))
		except AttributeError:
			self.__return_error("Did not find provider %s type %s" %(self.light_properties['provider'],
			self.light_properties['type']))

	@beartype
	def get_light_properties(self) -> dict[str, any]:
		"""
			Retrieves the properties for identfied light
			Responsible for:
				1. Opening the properties.json file for requested light
				2. Returns properties as a dictionary
		"""
		with open("%s/lights.json" %(self.settings['data_dir']),
		'r') as properties:
			properties_json = properties.read()
		properties = json.loads(properties_json)
		return properties[self.event_dict['name']]


	## Private methods

	@beartype
	def __return_error(self, reason: str) -> None:
		"""returns error to main debug channel"""
		producer = PalElement(self.settings['settings_file'])
		producer.send_txt(self.settings['debug_topic'], reason)
		producer.send_txt(self.event_dict['return_topic'], reason)
