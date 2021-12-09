"""
Description: Contains consumer class for media elements
"""
from typing import Dict, Union
import vlc
from beartype import beartype


class PalAudioPlayer():
	"""
		Description: Handles playing audio
		Responsible for:
			1. Initiating the VLC Player
			2. Controlling playback
	"""
	@beartype
	def __init__(self, options: str='') -> None:
		self.player = vlc.Instance(options)
		self.media_list = None
		self.media_list_player = None
		self.media = None
		self.control_dict = None

	@beartype
	def bye(self) -> None:
		"""Cleans up the the current player"""
		try:
			self.stop()
			self.media_list_player.get_media_player().release()
			del self.media
			del self.media_list_player
			self.player.release()
			del self.player
		except AttributeError:
			pass # do nothing we know this may blow up if something has not already started to play

	@beartype
	def set(self, control_dict: Dict[str, Union[str, int]]) -> None:
		"""
		Control the audio player. Requries:
			control_dict = Dictionary detailing what controls to execute
		"""
		self.control_dict = control_dict
		if 'play_track' in self.control_dict:
			self.__set_media()

		if 'volume' in self.control_dict:
			self.__set_volume()

		if 'play' in self.control_dict:
			self.__play_stop_pause()

		if 'loop' in self.control_dict:
			self.__set_loop()

## Private methods
	@beartype
	def __play_stop_pause(self) -> None:
		"""
			Starts or stops the player
		"""
		if self.control_dict['play'] == 'stop':
			self.media_list_player.get_media_player().stop()
		elif self.control_dict['play'] == 'play':
			self.media_list_player.play()
		elif self.control_dict['play'] == 'pause':
			self.media_list_player.pause()
		else:
			raise ValueError("Unknown play status: %s" %(self.control_dict['play']))

	@beartype
	def __set_loop(self) -> None:
		"""
			Manipulates looping
		"""
		self.player.vlm_set_loop("1", True)

	@beartype
	def __set_media(self) -> None:
		"""
			Sets the playing media
		"""
		# creating a new media list
		self.media_list = self.player.media_list_new()
		# creating a media player object
		self.media_list_player = self.player.media_list_player_new()
		# creating a new media
		self.media = self.player.media_new(self.control_dict['play_track'])
		# adding media to media list
		self.media_list.add_media(self.media)
		# setting media list to the mediaplayer
		self.media_list_player.set_media_list(self.media_list)


	@beartype
	def __set_volume(self) -> None:
		"""
			Adjusts the volume
		"""
		self.media_list_player.get_media_player().audio_set_volume(int(self.control_dict['volume']))
