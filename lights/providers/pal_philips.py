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

	@beartype
	def discover(self, light_properties: dict[str, dict[str, any]]) -> None:
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
	def set(self, event_dict: dict[str, any], light_properties: dict[str, any]) -> None:
		"""
		Set the status of a light.
		"""
		super().set(event_dict,light_properties)
		self.instance = self.light_properties['address']
		self.hue.load_existing()
		self.hue.fetch_lights()
		# Light must be turned on before manipulation
		self.__on_off()
		if self.event_dict['power']:
			# Currently only support the brightness adjustment
			self.__brightness()

	# Private functions
	@beartype
	def __brightness(self) -> None:
		"""Set brightness level."""
		self.hue.set_brightness(self.event_dict['brightness'])

	@beartype
	def __on_off(self) -> None:
		"""Power on or off a light."""
		if self.event_dict['power']:
			self.hue.turn_on(self.instance)
		else:
			self.hue.turn_off(self.instance)
