"""
Description: Module that supports Magic Hue lights
"""

import magichue
from lights.providers.light_type import LightType

class PalMagicHue(LightType):
	def __init__(self, settings):
		super().__init__(settings)

	def discover(self, light_properties):
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
			Returns a list of device dictionaries
		"""
		# Search for bulbs on the network
		for bulb in magichue.discover_bulbs():
			# Attempt to match each bulb to a light
			for light in light_properties:
				fields = bulb.split(",")
				# If type matches PalMagic and the identifier matches then set the address to the IP filied
				if 'PalMagicHue' == light_properties[light]['type'] and fields[1] == light_properties[light]['identifier']:
					light_properties[light]['address'] = fields[0]


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
