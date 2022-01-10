"""
Description: Dynamicly calls the required light class to handle the requested event
"""

import importlib
import json
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
	def __init__(self, settings, config_dict: dict[str, any]) -> None:
		"""Construct for the light event"""
		self.settings = settings
		self.config_dict = config_dict

class LightConfigEvent(ConfigEvent):
	"""
		Description: Updates the status of lights
		Responsible for:
			1. Parses the dictionary
			2. Locates the provider/module and the type of light
			3. iniates the light
			4. Contains method to push to Kafka as producer
	"""
	
	@beartype
	def __init__(self, settings, config_dict: dict[str, any]) -> None:
		"""Contruct for the light event"""
		self.settings = settings
		self.config_dict = config_dict
		self.light_properties = self.get_light_properties()

	@beartype
	def trigger(self) -> None:
		'''
			Trigger method
			Responsible for:
				1. Check request type
				2. Determine element
				3. Initiate correct call based on type and element
		'''
		if self.config_dict['preset']:
			self.__preset()
				
	## Private methods

	@beartype
	def __preset(self) -> None:
		pass

	@beartype
	def __return_error(self, reason: str) -> None:
		"""returns error to main debug channel"""
		producer = PalElement(self.settings['settings_file'])
		producer.send_txt(self.settings['debug_topic'], reason)
		producer.send_txt(self.event_dict['return_topic'], reason)
