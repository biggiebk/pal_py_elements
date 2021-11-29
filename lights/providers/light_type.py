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
		self.event_dict = {}
		self.light_properties = {}
		self.settings = settings

	def discover(self, light_properties):
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
		"""

	def brightness(self):
		"""Set brightness level."""

	def color_rgb(self):
		"""Set color using RGB"""

	def on_off(self):
		"""Power on or off a light."""

	def set_properties(self, light_properties):
		"""
		Set the light properties. Requries:
			light_properties = Dictionary of the light properties
		"""
		self.light_properties = light_properties

	def set_status(self, event_dict):
		"""
		Set the status of a light.
		"""
		self.event_dict = event_dict
