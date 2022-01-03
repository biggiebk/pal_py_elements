"""
Description: Module that supports Philips lights
"""
from beartype import beartype
from hue_api import HueApi
from lights.providers.light_type import LightType

class PalPhilips(LightType):
	"""Used to communicate with Philips devices"""
	def __init__(self, settings):
		super().__init__(settings)
		self.instance = None
		self.hue = HueApi()
		self.provider = 'lights.providers.pal_philips'
		self.type = 'PalPhilips'

	@beartype
	def brightness(self) -> None:
		"""Set brightness level."""
		self.hue.set_brightness(self.event_dict['brightness'])

	@beartype
	def discover(self) -> None:
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
		"""
		super().discover()
		# Retrieve list of philip lights
		self.hue.load_existing()
		# initiate iterator
		philips = iter(enumerate(self.hue.fetch_lights()))
		for index, philip in philips:
			# Attempt to match each light
			# Attempt to match each device to a light
			device = self._find_device_by_identifier(philip.name)
			self._update_device_address_by_name(device['name'], str(index))

	@beartype
	def on_off(self) -> None:
		"""Power on or off a light."""
		if self.event_dict['power']:
			self.hue.turn_on(self.instance)
		else:
			self.hue.turn_off(self.instance)


	@beartype
	def set(self, event_dict: dict[str, any], device_properties: dict[str, any]) -> None:
		"""
		Set the status of a light.
		"""
		super().set(event_dict,device_properties)
		self.instance = int(device_properties['address'])
		self.hue.load_existing()
		self.hue.fetch_lights()
		# Light must be turned on before manipulation
		self.on_off()
		if self.event_dict['power']:
			# Currently only support the brightness adjustment
			self.brightness()
		self.bye()
