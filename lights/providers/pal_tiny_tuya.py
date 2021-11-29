"""
Description: Module that supports Magic Hue lights
"""
import time
import tinytuya
from lights.providers.light_type import LightType

class PalTinyTuya(LightType):
	"""Used to communicate with Tuya devices"""
	def __init__(self, settings):
		super().__init__(settings)
		self.tiny_tuya = None

	def discover(self, light_properties):
		"""
			Responsible for discovering lights of this type.
			Requires:
				light_properties = A list of dictionaries containing light properties
		"""
		# Search for devices on the network
		tuyas = tinytuya.deviceScan(False, 50)
		for tuya in tuyas:
			# Attempt to match each device to a light
			for light in light_properties:
				# If type matches PalTinyTuya and the identifier matches then set the address to the IP
				if (light_properties[light]['type'] == 'PalTinyTuya'
				and tuyas[tuya]['gwId'] == light_properties[light]['identifier']):
					light_properties[light]['address'] = tuya


	def brightness(self):
		"""Set brightness level."""
		self.tiny_tuya.set_white(255,self.event_dict['brightness'])
		#time.sleep(1.0)
		#self.tiny_tuya.set_brightness(self.event_dict['brightness'])


	def color_rgb(self):
		"""Set color using RGB"""
		self.tiny_tuya.set_colour(self.event_dict['red'], self.event_dict['green'],
		self.event_dict['blue'])

	def on_off(self):
		"""Power on or off a light."""
		if self.event_dict['power']:
			self.tiny_tuya.turn_on()
		else:
			self.tiny_tuya.turn_off()


	def set_status(self, event_dict):
		"""
		Set the status of a light.
		"""
		super().set_status(event_dict)
		self.tiny_tuya = tinytuya.BulbDevice(self.light_properties['identifier'],
		self.light_properties['address'], self.light_properties['key'])
		self.tiny_tuya.set_version(3.3)
		if self.event_dict['power']:
			if (self.event_dict['red'] == -1 and self.event_dict['green'] == -1
			and self.event_dict['blue'] == -1):
				self.tiny_tuya.set_white(self.event_dict['brightness'],1000)
			else:
				self.color_rgb()
		self.on_off()
