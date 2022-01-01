"""
Description: Contains the Element parent class

"""

import json
from beartype import beartype
from kafka import KafkaConsumer, KafkaProducer

class PalElement():
	"""
		Description: Parent class used by elements.
		Responsible for:
			1. Basic constructor for starting elements.
			2. Initiates Kafka cosumer
			3. Contains method to push to Kafka as producer
	"""
	@beartype
	def __init__(self, settings_file: str) -> None:
		"""
			Construct for elemental classes.
			Responsible for:
				1. Loading settings.
				2. Initate topic consumer
			Requires:
				settings_file - Path to the elementals setting file
		"""
		self.settings_file = settings_file
		self.settings = {}
		self.__load_settings()
		self.settings['settings_file'] = settings_file
		self.consumer = None

	@beartype
	def listen(self) -> None:
		"""
			Description: Connects to Kafka and consumes a topic
			Responsible for:
				1. Connecting to Kafka and listening for events/messages
				2. Calls the process_event method
			Requires:
				Nothing
		"""
		self.consumer = KafkaConsumer(self.settings['listen_topic'],
			bootstrap_servers=self.settings['kafka_address'])
		for msg in self.consumer:
			self.process_event(msg)

	@beartype
	def process_event(self, consumer_message: tuple) -> None:
		"""
			Description: Each element should overide this method. The code here mostly
				is to support testing connectivity with Kafka
			Responsible for:
				1. Converts the messages value to string
				2. Returns the string
				3. Quits the class
			Requires:
				consuer_message
		"""
		print(f"{self.settings['listen_topic']} - {consumer_message.value.decode('utf-8')}")

	@beartype
	def reload(self):
		"""
			Reloads the element
				1. Reloads the configuration
		"""
		self.__load_settings()

	@beartype
	def send(self, topic, event_bytes: bytes) -> None:
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

	@beartype
	def send_txt(self, topic, text_message: str) -> None:
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

	@beartype
	def stop(self) -> None:
		"""Closes the the consumer and exits"""
		self.consumer.close()

	## Private methods, best not to overide anything beyond this point

	@beartype
	def __load_settings(self) -> None:
		"""
			Description: Parent class used by other elements.
			Responsible for:
				1. Loading settings
			Requires:
				settings_file - Path to the elementals setting file
		"""
		with open(self.settings_file, 'r', encoding='utf-8') as settings:
			settings_json = settings.read()
		self.settings = json.loads(settings_json)
