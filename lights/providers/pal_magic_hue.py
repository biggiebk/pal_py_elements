"""
Description: Module that supports Magic Hue lights
"""

import socket
import time
from beartype import beartype
import magichue
from lights.providers.light_type import LightType

class PalMagicHue(LightType):
	"""Used to communicate with Magic Hue/Home devices"""
	def __init__(self, settings):
		super().__init__(settings)
		self.magic_hue = None

	@beartype
	def discover(self, light_properties: dict[str, dict[str, any]]) -> None:
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
		"""
		super().discover(light_properties)
		# Search for bulbs on the network

		# The magichue library does not support identification of bulbs, so we have to code our own
		DISCOVERY_PORT = 48899
		DISCOVERY_MSG = b"HF-A11ASSISTHREAD"
		bulbs = []

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		sock.settimeout(1)
		sock.sendto(DISCOVERY_MSG, ('255.255.255.255', DISCOVERY_PORT))

		try:
			while True:
				response, bulb = sock.recvfrom(64)
				if response != DISCOVERY_MSG:
					bulbs.append(response.decode())
		except socket.timeout:
			pass

		sock.close()

		for bulb in bulbs:
			# Attempt to match each bulb to a light
			for light in light_properties:
				fields = bulb.split(",")
				# If type matches PalMagic and the identifier matches then set the address to the IP filied
				if (light_properties[light]['type'] == 'PalMagicHue'
				and fields[1] == light_properties[light]['identifier']):
					light_properties[light]['address'] = fields[0]

	@beartype
	def set(self, event_dict: dict[str, any], light_properties: dict[str, any]) -> None:
		"""
		Set the status of a light.
		"""
		super().set(event_dict,light_properties)
		self.magic_hue = magichue.Light(self.light_properties['address'])
		# If power is set to True
		if self.event_dict['power']:
			# if mode is white (R, G, and B all equal -1)
			if (self.event_dict['red'] == -1 and self.event_dict['green'] == -1
			and self.event_dict['blue'] == -1 ):
				self.__brightness()
			else:
				self.__color_rgb()
		self.__on_off()

	# Private functions
	@beartype
	def __brightness(self) -> None:
		"""Set brightness level."""
		self.event_dict['red'] = 255
		self.event_dict['green'] = 255
		self.event_dict['blue'] = 255
		self.__color_rgb()
		time.sleep(1.0)
		self.magic_hue.brightness = self.event_dict['brightness']

	@beartype
	def __color_rgb(self) -> None:
		"""Set color using RGB"""
		self.magic_hue.rgb = (self.event_dict['red'],
		self.event_dict['green'], self.event_dict['blue'])
		print(self.magic_hue.update_status)

	@beartype
	def __on_off(self) -> None:
		"""Power on or off a light."""
		self.magic_hue.on = self.event_dict['power']
