"""
Description: Dynamicly calls the required light class to handle the requested event
"""

import json
from pal_element_producer import PalElementProducer

class LightEvent():

	"""
		Description: Updates the status of lights
		Responsible for:
			1. Parses the JSON
			1. Locates the provider/module and the type of light
			2. iniates the light
			3. Contains method to push to Kafka as producer
	"""

	def __init__(self, settings, event_dict):
		"""Contruct for the light event"""
		self.settings = settings
		self.event_dict = event_dict
		self.light_properties = self.__get_light_properties()

	def trigger(self):
		'''
			Trigger method
			Responsible for:
				1. Locating the provider modules
				2. Initiating the requested light class
				3. If error send update back to originator
		'''
		#Converter the provider name to a module
		module = __import__(self.light_properties['provider'])

		# Load the class
		try:
			light = getattr(module, self.light_properties['type'])
			light.new(self.settings, self.light_properties, self.event_dict)
			light.set_status()
		except ModuleNotFoundError:
			self.__return_error("Unable to locate provider: %s" %(self.light_properties['provider']))
		except AttributeError:
			self.__return_error("Did not find provider %s type %s" %(self.light_properties['provider'],
			self.light_properties['type']))


	## Private methods
	def __get_light_properties(self):
		"""
			Retrieves the properties for identfied light
			Responsible for:
				1. Opening the properties.json file for requested light
				2. Returns properties as a dictionary
		"""
		with open("%s/devices/lights/%s" %(self.settings['data_dir'], self.event_dict['name']),
		'r') as properties:
			properties_json = properties.read()
		return json.loads(properties_json)


	def __return_error(self, reason):
		"""returns error to calling client"""
		producer = PalElementProducer(self.settings['settings_file'])
		producer.send_txt(self.settings['debug_topic'], reason)
