import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VolumeControl:

	def __init__(self):
		self.devices = AudioUtilities.GetSpeakers()
		self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
		self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
		self.volume_range = self.volume.GetVolumeRange()
		self.min_volume = self.volume_range[0]
		self.max_volume = self.volume_range[1]

	def set_volume_control(self, distance):
		"""Устанавливает громкость в зависимости от дистанции между пальцами."""
		vol = int(np.interp(distance, [10,170], [self.min_volume, self.max_volume]))
		self.volume.SetMasterVolumeLevel(vol, None)

		return vol