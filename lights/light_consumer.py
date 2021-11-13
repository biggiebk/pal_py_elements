"""
Description: Contains consumer class for light elements
"""
import threading
import json

from pal_element_consumer import PalElementConsumer
from lights.light_event import LightEvent


class LightConsumer(PalElementConsumer):
	"""
		Description: Parent class used by other elements.
		Responsible for:
			1. Basic constructor for starting elements.
			2. Initiates Kafka cosumer
			3. Contains method to push to Kafka as producer
	"""

	def __init__(self, settings_file):
		super().__init__(settings_file=settings_file)

	def process_event(self, consumer_message):
		"""
			Description: Initiats events for the requested light
			Responsible for:
				1. Converts the messages value to dictionary
				2. Runs the light event as a daemon thread
			Requires:
				consumer_message
		"""
		light_event = LightEvent(self.settings,json.loads(consumer_message.value.decode("utf-8")))
		thread = threading.Thread(target=light_event.trigger(), args=())
		thread.setDaemon(True)
		thread.start()
