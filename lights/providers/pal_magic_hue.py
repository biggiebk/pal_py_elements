"""
Description: Module that supports Magic Hue lights
"""

import time
from typing import Dict, Any
from beartype import beartype
import magichue
from lights.providers.light_type import LightType

class PalMagicHue(LightType):
	"""Used to communicate with Magic Hue/Home devices"""
	def __init__(self, settings):
		super().__init__(settings)
		self.magic_hue = None

	@beartype
	def discover(self, light_properties: Dict[str, Dict[str, Any]]) -> None:
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
		"""
		super().discover(light_properties)
		# Search for bulbs on the network
		for bulb in magichue.discover_bulbs():
			# Attempt to match each bulb to a light
			for light in light_properties:
				fields = bulb.split(",")
				# If type matches PalMagic and the identifier matches then set the address to the IP filied
				if (light_properties[light]['type'] == 'PalMagicHue'
				and fields[1] == light_properties[light]['identifier']):
					light_properties[light]['address'] = fields[0]

	@beartype
	def brightness(self) -> None:
		"""Set brightness level."""
		self.event_dict['red'] = 255
		self.event_dict['green'] = 255
		self.event_dict['blue'] = 255
		self.color_rgb()
		time.sleep(1.0)
		self.magic_hue.brightness = self.event_dict['brightness']

	@beartype
	def color_rgb(self) -> None:
		"""Set color using RGB"""
		self.magic_hue.rgb = (self.event_dict['red'],
		self.event_dict['green'], self.event_dict['blue'])
		print(self.magic_hue.update_status)

	@beartype
	def on_off(self) -> None:
		"""Power on or off a light."""
		self.magic_hue.on = self.event_dict['power']

	@beartype
	def set_status(self, event_dict: Dict[str, Any]) -> None:
		"""
		Set the status of a light.
		"""
		super().set_status(event_dict)
		self.magic_hue = magichue.Light(self.light_properties['address'])
		# If power is set to True
		if self.event_dict['power']:
			# if mode is white (R, G, and B all equal -1)
			if (self.event_dict['red'] == -1 and self.event_dict['green'] == -1
			and self.event_dict['blue'] == -1 ):
				self.brightness()
			else:
				self.color_rgb()
		self.on_off()
