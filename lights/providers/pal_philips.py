"""
Description: Module that supports Philips lights
"""

from hue_api import HueApi
from lights.providers.light_type import LightType

class PalPhilips(LightType):
	"""Used to communicate with Philips devices"""
	def __init__(self, settings):
		super().__init__(settings)
		self.instance = None
		self.hue = HueApi()

	def discover(self, light_properties):
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
		"""
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

	def brightness(self):
		"""Set brightness level."""
		self.hue.set_brightness(self.event_dict['brightness'])

	def on_off(self):
		"""Power on or off a light."""
		if self.event_dict['power']:
			self.hue.turn_on(self.instance)
		else:
			self.hue.turn_off(self.instance)


	def set_status(self, event_dict):
		"""
		Set the status of a light.
		"""
		self.instance = self.light_properties['address']
		self.hue.load_existing()
		self.hue.fetch_lights()
		super().set_status(event_dict)
		# Light must be turned on before manipulation
		self.on_off()
		if self.event_dict['power']:
			# Currently only support the brightness adjustment
			self.brightness()
