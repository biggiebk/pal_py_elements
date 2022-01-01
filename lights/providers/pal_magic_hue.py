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
	def brightness(self) -> None:
		"""Set brightness level."""
		self.event_dict['red'] = 255
		self.event_dict['green'] = 255
		self.event_dict['blue'] = 255
		self.color_rgb()
		time.sleep(1.0)
		self.magic_hue.brightness = self.event_dict['brightness']

	@beartype
	def color_rgb(self) -> None:
		"""Set color using RGB"""
		self.magic_hue.rgb = (self.event_dict['red'],
		self.event_dict['green'], self.event_dict['blue'])
		print(self.magic_hue.update_status)

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
		discover_port = 48899
		discovery_message = b"HF-A11ASSISTHREAD"
		bulbs = []

		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		sock.settimeout(1)
		sock.sendto(discovery_message, ('255.255.255.255', discover_port))

		try:
			while True:
				response, bulb = sock.recvfrom(64)
				if response != discovery_message:
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
	def on_off(self) -> None:
		"""Power on or off a light."""
		self.magic_hue.on = self.event_dict['power']

	@beartype
	def set(self, event_dict: dict[str, any], light_properties: dict[str, any]) -> None:
		"""
		Set the status of a light.
		"""
		self.magic_hue = magichue.Light(light_properties['address'])
		super().set(event_dict,light_properties)
