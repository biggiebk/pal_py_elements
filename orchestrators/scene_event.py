"""
Description: Module containing the config preset classes
"""

import json
from pymongo import MongoClient
from beartype import beartype
from pal_element import PalElement

class SceneEvent():
	"""
		Description: Scene events class
		Responsible for:
			1. Establishes a standard construct
			2. Retrieve scene name from DB
			3. Initiate elemental updates
	"""

	@beartype
	def __init__(self, settings: dict[str, any]) -> None:
		"""Construct for the scene event"""
		self.settings = settings
		self.pal_mongo = MongoClient(self.settings['database']['db_host'],
			self.settings['database']['db_port'], username=self.settings['database']['ele_user'],
			password=self.settings['database']['ele_password'])
		self.pal_db = self.pal_mongo[self.settings['database']['ele_db_name']]
		self.pal_scenes = self.pal_db['scene_presets']
		self.pal_light_presets = self.pal_db['light_presets']
		self.pal_device_cfgs = self.pal_db['device_cfgs']
		self.pal_audio_presets = self.pal_db['audio_presets']

	@beartype
	def trigger(self, params: dict[str, any]) -> None:
		"""Retrieves scene from DB and initiates the updates"""
		find_scene = {'name': params['name']}
		scene = self.pal_scenes.find_one(find_scene)
		if len(scene) == 1:
			self.process(scene)
		else: # return error
			self._return_error(params, "Scenario not found")

	@beartype
	def process(self, scene: dict[str, any])-> None:
		"""Process the event elemental changes"""
		if 'lights' in scene:
			for device_name, preset_name in scene['lights'].items():
				event = self.pal_light_presets.find_one({'name': preset_name})
				event[0].pop('_id')
				event['name'] = device_name
				event['event_type'] = 'control'
				self._submit_event(event, 'elemental_lights')
		if 'audio' in scene:
			event = self.pal_audio_presets.find_one({'name': scene['audio']})
			event[0].pop('_id')
			event['name'] = device_name
			event['event_type'] = 'control'
			self._submit_event(event, 'elemental_audio')


## Private methods

	@beartype
	def _return_error(self, params, error_text: str) -> None:
		"""returns error to main debug channel"""
		error = {}
		error['session'] = params['session']
		error['tracking_id'] = params['tracking_id']
		error['error_text'] = error_text
		text = json.dumps(error)
		producer = PalElement(self.settings['settings_file'])
		producer.send_txt(self.settings['debug_topic'], text)
		producer.send_txt(params['return_topic'], text)

	@beartype
	def _submit_event(self, event: dict[str, any], topic_name: str) -> None:
		"""submit the elemental event"""
		text = json.dumps(event)
		producer = PalElement(self.settings['settings_file'])
		producer.send_txt(self.settings[topic_name], text)
