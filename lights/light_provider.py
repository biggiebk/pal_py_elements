"""
Description: Contains the LightProvider parent class

"""

class LightProvider():
	"""
		Description: Parent class used by light providers.
		Responsible for:
			1. Basic constructor for providers.
			2. Establishes basic
			3. Contains method to push to Kafka as producer
	"""
	def __init__(self, settings, light_properties, event_dict):
		self.settings = settings
		self.light_properties = light_properties
		self.event_dict = event_dict

	def brightness(self):
		"""
		Set brightness level. Requries:
			brightness_level = number indicating brightness level
		"""

	def color_rgb(self):
		"""
		Set color using RGB
			red = number value for level of red
			green = number value for level of green
			blue = number value for level of blue
		"""

	def flip(self):
		"""Quickly flip a light on and off"""

	def on_off(self):
		"""
		Power on or off a light. Requires:
			power = boolean value for on (True) or off (False)
		"""

	def set_status(self):
		"""
		Set the status of a light. Requires:
			power = boolean value for on (True) or off (False)
			brightness_level = number indicating brightness level
			red = number value for level of red
			green = number value for level of green
			blue = number value for level of blue
		"""
		if self.event_dict['power']:
			self.color_rgb()
			self.brightness()
		self.on_off()
