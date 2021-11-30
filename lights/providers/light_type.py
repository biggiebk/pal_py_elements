"""
Description: Contains the LightProvider parent class

"""
from typing import Dict, Any
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
	def discover(self, light_properties: Dict[str, Dict[str, Any]]) -> None:
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
		"""

	def brightness(self) -> None:
		"""Set brightness level."""

	def color_rgb(self) -> None:
		"""Set color using RGB"""

	def on_off(self) -> None:
		"""Power on or off a light."""

	def set_properties(self, light_properties: Dict[str, Any]) -> None:
		"""
		Set the light properties. Requries:
			light_properties = Dictionary of the light properties
		"""
		self.light_properties = light_properties

	def set_status(self, event_dict: Dict[str, Any]) -> None:
		"""
		Set the status of a light.
		"""
		self.event_dict = event_dict
