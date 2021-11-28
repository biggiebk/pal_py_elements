"""
Description: Module that supports Magic Hue lights
"""

import tinytuya
from lights.providers.light_type import LightType

class PalTinyTuya(LightType):
	def __init__(self, settings):
		super().__init__(settings)

	def discover(self, light_properties):
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
			Returns a list of device dictionaries
		"""
		# Search for devices on the network
		tuyas = tinytuya.deviceScan(False, 50)
		for tuya in tuyas:
			# Attempt to match each device to a light
			for light in light_properties:
				# If type matches PalTinyTuya and the identifier matches then set the address to the IP
				if 'PalTinyTuya' == light_properties[light]['type'] and tuyas[tuya]['gwId'] == light_properties[light]['identifier']:
					light_properties[light]['address'] = tuya


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