"""
Description: Orchestrators for Python Elements

"""
import threading
import json
from beartype import beartype
from pal_element import PalElement
from config_events import LightConfigEvent, AudioConfigEvent, SceneConfigEvent

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
	def __init__(self, settings_file: str) -> None:
		super().__init__(settings_file=settings_file)

	@beartype
	def process_event(self, consumer_message: tuple) -> None:
		"""
			Description: Initiats events for the requested light
			Responsible for:
				1. Converts the messages value to dictionary
				2. Checks for element type
				3. Initiates the correct config event
			Requires:
				consumer_message
		"""
		config_dict = json.loads(consumer_message.value.decode("utf-8"))
		if config_dict['element'] == 'light':
			light_config_event = LightConfigEvent(self.settings, config_dict)
			thread = threading.Thread(target=light_config_event.trigger(), args=())
			thread.setDaemon(True)
			thread.start()
		elif config_dict['element'] == 'audio':
			audio_config_event = AudioConfigEvent(self.settings, config_dict)
			thread = threading.Thread(target=audio_config_event.trigger(), args=())
			thread.setDaemon(True)
			thread.start()
		elif config_dict['element'] == 'scene':
			scene_config_event = SceneConfigEvent(self.settings, config_dict)
			thread = threading.Thread(target=scene_config_event.trigger(), args=())
			thread.setDaemon(True)
			thread.start()
		else:
			pass
