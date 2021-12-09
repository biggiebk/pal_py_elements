"""
Description: Module that supports Magic Hue lights
"""
from typing import Dict, Any
from beartype import beartype
import tinytuya
from lights.providers.light_type import LightType

class PalTinyTuya(LightType):
	"""Used to communicate with Tuya devices"""
	def __init__(self, settings):
		super().__init__(settings)
		self.tiny_tuya = None

	@beartype
	def discover(self, light_properties: Dict[str, Dict[str, Any]]) -> None:
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
		"""
		super().discover(light_properties)
		# Search for devices on the network
		tuyas = tinytuya.deviceScan(False, 50)
		for tuya in tuyas:
			# Attempt to match each device to a light
			for light in light_properties:
				# If type matches PalTinyTuya and the identifier matches then set the address to the IP
				if (light_properties[light]['type'] == 'PalTinyTuya'
				and tuyas[tuya]['gwId'] == light_properties[light]['identifier']):
					light_properties[light]['address'] = tuya


	@beartype
	def set(self, event_dict: Dict[str, Any], light_properties: Dict[str, Any]) -> None:
		"""
		Set the status of a light.
		"""
		super().set(event_dict,light_properties)
		self.tiny_tuya = tinytuya.BulbDevice(self.light_properties['identifier'],
		self.light_properties['address'], self.light_properties['key'])
		self.tiny_tuya.set_version(3.3)
		if self.event_dict['power']:
			if (self.event_dict['red'] == -1 and self.event_dict['green'] == -1
			and self.event_dict['blue'] == -1):
				self.tiny_tuya.set_white(self.event_dict['brightness'],1000)
			else:
				self.__color_rgb()
		self.__on_off()

	# Private functions
	@beartype
	def __brightness(self):
		"""Set brightness level."""
		self.tiny_tuya.set_white(255,self.event_dict['brightness'])

	@beartype
	def __color_rgb(self) -> None:
		"""Set color using RGB"""
		self.tiny_tuya.set_colour(self.event_dict['red'], self.event_dict['green'],
		self.event_dict['blue'])

	@beartype
	def __on_off(self) -> None:
		"""Power on or off a light."""
		if self.event_dict['power']:
			self.tiny_tuya.turn_on()
		else:
			self.tiny_tuya.turn_off()
