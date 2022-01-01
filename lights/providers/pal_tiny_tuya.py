"""
Description: Module that supports Magic Hue lights
"""

from beartype import beartype
import tinytuya
from lights.providers.light_type import LightType

class PalTinyTuya(LightType):
	"""Used to communicate with Tuya devices"""
	def __init__(self, settings):
		super().__init__(settings)
		self.tiny_tuya = None

	@beartype
	def brightness(self):
		"""Set brightness level."""
		self.tiny_tuya.set_white(self.event_dict['brightness'],1000)

	@beartype
	def color_rgb(self) -> None:
		"""Set color using RGB"""
		self.tiny_tuya.set_colour(self.event_dict['red'], self.event_dict['green'],
		self.event_dict['blue'])

	@beartype
	def discover(self, light_properties: dict[str, dict[str, any]]) -> None:
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
		"""
		super().discover(light_properties)
		# Search for devices on the network
		tuyas = tinytuya.deviceScan(False, 50)
		for tuya in tuyas.items():
			# Attempt to match each device to a light
			for light in light_properties:
				# If type matches PalTinyTuya and the identifier matches then set the address to the IP
				if (light_properties[light]['type'] == 'PalTinyTuya'
				and tuya[1]['gwId'] == light_properties[light]['identifier']):
					light_properties[light]['address'] = tuya[0]

	@beartype
	def on_off(self) -> None:
		"""Power on or off a light."""
		if self.event_dict['power']:
			self.tiny_tuya.turn_on()
		else:
			self.tiny_tuya.turn_off()

	@beartype
	def set(self, event_dict: dict[str, any], light_properties: dict[str, any]) -> None:
		"""
		Set the status of a light.
		"""
		self.tiny_tuya = tinytuya.BulbDevice(light_properties['identifier'],
		light_properties['address'], light_properties['key'])
		self.tiny_tuya.set_version(3.3)
		super().set(event_dict,light_properties)
