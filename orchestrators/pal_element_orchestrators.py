"""
Description: Orchestrators for Python Elements

"""
import threading
import json
from beartype import beartype
from pal_element import PalElement
from orchestrators.config_event import ConfigEvent

class PalElementConfigOrchestrator(PalElement):
	"""
		Description: Responsible for distrobuting requests for elements
		Responsible for:
			1. Determing element type
			2. Request type (update or status)
			3. Retrieving additional related informaton
			4. Submiting the request to the element
	"""

	@beartype
	def process_event(self, consumer_message: tuple) -> None:
		"""
			Description: Process configuration events
			Responsible for:
				1. Converts the message to dictionary
				2. Checks for element type
				3. Initiates the correct config event
			Requires:
				consumer_message
		"""
		params = json.loads(consumer_message.value.decode("utf-8"))
		print(f"{params['element']}_{params['request_type']}")
		light_config_preset = ConfigEvent(self.settings, f"{params['element']}_{params['request_type']}")
		thread = threading.Thread(target=light_config_preset.trigger, args=([params]))
		thread.setDaemon(True)
		thread.start()
