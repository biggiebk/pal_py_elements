"""
Description: Contains the LightProvider parent class

"""

class LightType():
	"""
		Description: Parent class used by light providers.
		Responsible for:
			1. Basic constructor for providers.
			2. Establishes basic
			3. Contains method to push to Kafka as producer
	"""
	def __init__(self, settings):
		self.settings = settings
		self.light_properties = {}
		self.event_dict = {}

	def discover(self):
		"""
			Responsible for discovering lights of this type.
			Returns a list of device dictionaries
		"""

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
		self.light_properties = light_properties
		self.event_dict = event_dict
		if self.event_dict['power']:
			self.color_rgb()
			self.brightness()
		self.on_off()
