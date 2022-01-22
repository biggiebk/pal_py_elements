"""
Description: Contains the LightProvider parent class
"""
import datetime
from beartype import beartype
from pymongo import MongoClient

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
		self.device_properties = {}
		self.settings = settings
		self.provider = None
		self.type = None
		self.pal_mongo = None
		self.ele_db = None

	@beartype
	def brightness(self) -> None:
		"""Set brightness level."""


	@beartype
	def bye(self) -> None:
		"""Clean up and exit"""
		if self.pal_mongo is not None:
			self.pal_mongo.close()

	@beartype
	def color_rgb(self) -> None:
		"""Set color using RGB"""

	@beartype
	def discover(self) -> None:
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
		"""

	@beartype
	def get_device_by_name(self, name: str) -> dict:
		"""
		Get device by indentifier, provider, and type
		"""
		self._connect_db()
		ele_db = self.pal_mongo[self.settings['database']['ele_db_name']]
		light_devices = ele_db['device_cfgs']
		device = light_devices.find_one({"name": name})

		# return the result
		return device

	@beartype
	def on_off(self) -> None:
		"""Power on or off a light."""

	@beartype
	def set(self, event_dict: dict[str, any], device_properties: dict[str, any]) -> None:
		"""
		Set the status of a light.
		"""
		self.event_dict = event_dict
		self.device_properties = device_properties
		if self.event_dict['power']:
			# if mode is white (R, G, and B all equal -1)
			if (self.event_dict['red'] == -1 and self.event_dict['green'] == -1
			and self.event_dict['blue'] == -1):
				self.brightness()
			else:
				self.color_rgb()
		self.on_off()

	## Private functions

	@beartype
	def _connect_db(self) -> None:
		if self.pal_mongo is None:
			self.pal_mongo = MongoClient(self.settings['database']['db_host'],
				self.settings['database']['db_port'], username=self.settings['database']['ele_user'],
				password=self.settings['database']['ele_password'])

	@beartype
	def _create_unknown_device(self, identifier: str) -> dict[str, any]:
		"""
		Create a recently discovered device
		"""
		# Create a new device
		self._connect_db()
		ele_db = self.pal_mongo[self.settings['database']['ele_db_name']]
		light_devices = ele_db['device_cfgs']
		device = {}
		device['name'] = datetime.datetime.today().strftime(f"Unknown_{self.type}" +
			'-%H-%M-%S-%f-%b-%d-%Y')
		device['identifier'] = identifier
		device['provider'] = self.provider
		device['type'] = self.type
		device['room'] = "Unknown"
		device['property'] = "Unknown"
		device['device_type'] = "Unknown"
		device['address'] = ""
		# add to the database
		light_devices.insert_one(device)
		return device

	@beartype
	def _find_device_by_identifier(self, identifier: str) -> dict[str, any]:
		"""
		Get device by indentifier, provider, and type
		"""
		self._connect_db()
		ele_db = self.pal_mongo[self.settings['database']['ele_db_name']]
		light_devices = ele_db['device_cfgs']
		search = {}
		search['identifier'] = identifier
		search['provider'] = self.provider
		search['type'] = self.type
		device = light_devices.find_one(search)
		# Make sure we found something if not create the unknown device
		if device is None:
			device = self._create_unknown_device(identifier)

		# return the result
		return device

	@beartype
	def _update_device_address_by_name(self, name: str, address: str) -> None:
		"""
		Update the device with an address using the name
		"""
		self._connect_db()
		ele_db = self.pal_mongo[self.settings['database']['ele_db_name']]
		light_devices = ele_db['device_cfgs']
		light_devices.update_one({"name": name}, {'$set': {"address": address}})
