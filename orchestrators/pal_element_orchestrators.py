"""
Description: Orchestrators for Python Elements

"""
import threading
import json
from beartype import beartype
from pal_element import PalElement
from orchestrators.config_event import ConfigEvent
from orchestrators.scene_event import SceneEvent

class PalElementConfigOrchestrator(PalElement):
	"""
		Description: Responsible for handing configuration updates for elements
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
				2. Initiates config event
			Requires:
				consumer_message
		"""
		params = json.loads(consumer_message.value.decode("utf-8"))
		config_event = ConfigEvent(self.settings, f"{params['element']}_{params['request_type']}")
		thread = threading.Thread(target=config_event.trigger, args=([params]))
		thread.setDaemon(True)
		thread.start()

class PalElementSceneOrchestrator(PalElement):
	"""
		Description: Responsible for distrobuting requests for elements
		Responsible for:
			1. Process scene
			2. Initiate updates to various elements
	"""

	def __init__(self, settings_file: str) -> None:
		super().__init__(settings_file)
		self.scene_event = SceneEvent(self.settings)

	@beartype
	def process_event(self, consumer_message: tuple) -> None:
		"""
			Description: Process configuration events
			Responsible for:
				1. Converts the message to dictionary
				2. Initiates the correct config event
			Requires:
				consumer_message
		"""
		params = json.loads(consumer_message.value.decode("utf-8"))
		self.scene_event.trigger(params)
