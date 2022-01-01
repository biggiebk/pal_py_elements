"""
Description: Contains the LightProvider parent class

"""
from beartype import beartype

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

	@beartype
	def brightness(self) -> None:
		"""Set brightness level."""

	@beartype
	def color_rgb(self) -> None:
		"""Set color using RGB"""

	@beartype
	def discover(self, light_properties: dict[str, dict[str, any]]) -> None:
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
		"""

	@beartype
	def on_off(self) -> None:
		"""Power on or off a light."""

	@beartype
	def set(self, event_dict: dict[str, any], light_properties: dict[str, any]) -> None:
		"""
		Set the status of a light.
		"""
		self.event_dict = event_dict
		self.light_properties = light_properties
		if self.event_dict['power']:
			# if mode is white (R, G, and B all equal -1)
			if (self.event_dict['red'] == -1 and self.event_dict['green'] == -1
			and self.event_dict['blue'] == -1):
				self.brightness()
			else:
				self.color_rgb()
		self.on_off()
