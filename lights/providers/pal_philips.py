"""
Description: Module that supports Philips lights
"""

from hue_api import HueApi
from lights.providers.light_type import LightType

class PalPhilips(LightType):
	def __init__(self, settings):
		super().__init__(settings)
		self.HUEAPI = HueApi()

	def discover(self, light_properties):
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
			Returns a list of device dictionaries
		"""
		# Retrieve list of philip lights
		self.HUEAPI.load_existing()
		# initiate iterator
		philips = iter(enumerate(self.HUEAPI.fetch_lights()))
		for index, philip in philips:
			# Attempt to match each light
			for light in light_properties:
				# If type matches PalPhilips and the identifier matches then set the address to the index/instance number
				if 'PalPhilips' == light_properties[light]['type'] and philip.name == light_properties[light]['identifier']:
					light_properties[light]['address'] = index

	def brightness(self):
		"""Set brightness level."""

	def color_rgb(self):
		"""Set color using RGB"""

	def on_off(self):
		"""Power on or off a light."""

	def set_status(self, light_properties, event_dict):
		"""
		Set the status of a light.
		"""
		if self.event_dict['power']:
			self.color_rgb()
			self.brightness()
		self.on_off()