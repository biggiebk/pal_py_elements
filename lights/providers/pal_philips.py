"""
Description: Module that supports Philips lights
"""

from typing import Dict, Any
from beartype import beartype
from hue_api import HueApi
from lights.providers.light_type import LightType

class PalPhilips(LightType):
	"""Used to communicate with Philips devices"""
	def __init__(self, settings):
		super().__init__(settings)
		self.instance = None
		self.hue = HueApi()

	@beartype
	def discover(self, light_properties: Dict[str, Dict[str, Any]]) -> None:
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
		"""
		super().discover(light_properties)
		# Retrieve list of philip lights
		self.hue.load_existing()
		# initiate iterator
		philips = iter(enumerate(self.hue.fetch_lights()))
		for index, philip in philips:
			# Attempt to match each light
			for light in light_properties:
				# If type matches PalPhilips and the identifier matches
				# then set the address to the index/instance number
				if (light_properties[light]['type'] == 'PalPhilips'
				and philip.name == light_properties[light]['identifier']):
					light_properties[light]['address'] = index

	@beartype
	def brightness(self) -> None:
		"""Set brightness level."""
		self.hue.set_brightness(self.event_dict['brightness'])

	@beartype
	def on_off(self) -> None:
		"""Power on or off a light."""
		if self.event_dict['power']:
			self.hue.turn_on(self.instance)
		else:
			self.hue.turn_off(self.instance)


	@beartype
	def set_status(self, event_dict: Dict[str, Any]) -> None:
		"""
		Set the status of a light.
		"""
		super().set_status(event_dict)
		self.instance = self.light_properties['address']
		self.hue.load_existing()
		self.hue.fetch_lights()
		# Light must be turned on before manipulation
		self.on_off()
		if self.event_dict['power']:
			# Currently only support the brightness adjustment
			self.brightness()
