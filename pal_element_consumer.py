"""
Description: Contains the Element parent class
"""

from kafka import KafkaConsumer
from pal_element import Pal_Element

class Pal_Element_Consumer(Pal_Element):
	"""
		Description: Parent class used by other elements.
		Responsible for:
			1. Basic constructor for starting elements.
			2. Initiates Kafka cosumer
			3. Contains method to push to Kafka as producer
	"""

	def listen(self):
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
