"""
Description: Contains the Element parent class

"""

from kafka import KafkaProducer
from pal_element import PalElement

class PalElementProducer(PalElement):
	"""
		Description: Parent class used by other producer elements.
	"""
	def __init__(self, settings_file):
		super().__init__(settings_file=settings_file)

	def send(self, topic, event_bytes):
		"""
			Description: Sends a byte array to Kafka as a producer
			Responsible for:
				1. Send event bytes to topic
			Requires:
				1. topic - Name of the topic to send message/event to (string)
				2. event_bytes - array of bytes
		"""
		producer = KafkaProducer(bootstrap_servers=self.settings['kafka_address'])
		producer.send(topic, event_bytes)
		producer.flush()

	def send_txt(self, topic, text_message):
		"""
			Description: Sends a text (string) to Kafka as a producer
			Responsible for:
				1. Convert the message to bytes from string
				2. Calls send
			Requires:
				1. topic - Name of the topic to send message/event to (string)
				2. text_message - Text message to send (string)
		"""
		self.send(topic, bytes(text_message, 'utf-8'))
