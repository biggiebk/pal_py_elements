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
		self.provider = 'lights.providers.pal_tiny_tuya'
		self.type = 'PalTinyTuya'

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
	def discover(self) -> None:
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
		"""
		super().discover()
		# Search for devices on the network
		tuyas = tinytuya.deviceScan(False, 5)
		for tuya in tuyas.items():
			# Attempt to match each device to a light
			device = self._find_device_by_identifier(tuya[1]['gwId'])
			self._update_device_address_by_name(device['name'],tuya[0])

	@beartype
	def on_off(self) -> None:
		"""Power on or off a light."""
		if self.event_dict['power']:
			self.tiny_tuya.turn_on()
		else:
			self.tiny_tuya.turn_off()

	@beartype
	def set(self, event_dict: dict[str, any], device_properties: dict[str, any]) -> None:
		"""
		Set the status of a light.
		"""
		self.tiny_tuya = tinytuya.BulbDevice(device_properties['identifier'],
		device_properties['address'], device_properties['auth']['key'])
		self.tiny_tuya.set_version(3.3)
		super().set(event_dict,device_properties)
		self.bye()
