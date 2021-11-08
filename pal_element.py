"""
Description: Contains the Element parent class

"""

import json

from kafka import KafkaConsumer
from kafka import KafkaProducer

class Pal_Element():
	"""
		Description: Parent class used by other elements.
		Responsible for:
			1. Basic constructor for starting elements.
			2. Initiates Kafka cosumer
			3. Contains method to push to Kafka as producer
	"""

	def __init__(self, settings_file):
		"""
			Construct for elemental classes.
			Responsible for:
				1. Loading settings.
				2. Initate topic consumer
			Requires:
				settings_file - Path to the elementals setting file
		"""
		self.settings = {}
		self.__load_settings(settings_file)

	def consumer(self):
		"""
			Description: Connects to Kafka and consumes a topic
			Responsible for:
				1. Connecting to Kafka and listening for events/messages
				2. Calls the event method
			Requires:
				Nothing
		"""
		consumer = KafkaConsumer(self.settings['topic'], bootstrap_servers=self.settings['address'])
		for msg in consumer:
			self.process_event(msg)

	def process_event(self, consumer_message):
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
		print("%s - %s" %(self.settings['topic'], consumer_message.value.decode("utf-8")))

	def producer(self, topic, text_message):
		"""
			Description: Pushes a message/event to Kafka as a producer
			Responsible for:
				1. Convert the message to bytes from string
				2. Send message to topic
			Requires:
				1. topic - Name of the topic to send message/event to (string)
				2. text_message - Text message to send (string)
		"""
		producer = KafkaProducer(bootstrap_servers=self.settings['address'])
		producer.send(topic, bytes(text_message, 'utf-8'))
		producer.flush()

	## Private classes, best not to overide anything beyond this point

	def __load_settings(self, settings_file):
		"""
			Description: Parent class used by other elements.
			Responsible for:
				1. Loading settings
			Requires:
				settings_file - Path to the elementals setting file
		"""
		with open(settings_file, 'r') as settings:
			settings_json = settings.read()
		# parse file
		self.settings = json.loads(settings_json)
