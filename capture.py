import cv2
import math
import mediapipe as mp
import sounddevice as sd
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
	

class HandGestureAudioControl:
	"""
	Обрабатывает жесты рук, определяет расстояние между указательным и большим пальцами,
	и управляет громкостью аудио в зависимости от этого расстояния.
	"""

	def __init__(self):
		self.devices = AudioUtilities.GetSpeakers()
		self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
		self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))
		self.volume_range = self.volume.GetVolumeRange()
		self.min_volume = self.volume_range[0]
		self.max_volume = self.volume_range[1]
		self.hands = mp.solutions.hands.Hands(max_num_hands=1)
		self.draw = mp.solutions.drawing_utils	

	def set_volume_control(self, distance):
		"""Устанавливает громкость в зависимости от дистанции между пальцами."""
		vol = int(np.interp(distance, [10,170], [self.min_volume, self.max_volume]))
		self.volume.SetMasterVolumeLevel(vol, None)

		return vol

	def get_finger_distance(self, hand_lms, w, h):
		"""Вычисляет расстояние между указательным и большим пальцами."""
		thumb_x, thumb_y = int(hand_lms.landmark[4].x * w), int(hand_lms.landmark[4].y * h)
		index_x, index_y = int(hand_lms.landmark[8].x * w), int(hand_lms.landmark[8].y * h)
		distance = int(math.sqrt((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2))

		return distance


	def hand_control(self, image, imageRGB):
		"""Обрабатывает жест руки и управляет громкостью."""
		h, w, _ = image.shape
		results = self.hands.process(imageRGB)

		if results.multi_hand_landmarks:
			for hand_lms in results.multi_hand_landmarks:
				for id, lm in enumerate(hand_lms.landmark):
					h, w, _ = image.shape
					cx, cy = int(lm.x * w), int(lm.y * h)
					cv2.putText(image, f'{id}', (cx, cy), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1, cv2.LINE_AA)

				distance = self.get_finger_distance(hand_lms, w, h)
				cv2.putText(image, f'Distance: {distance}', (30, 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1, cv2.LINE_AA)

				self.draw.draw_landmarks(image, hand_lms, mp.solutions.hands.HAND_CONNECTIONS)

				audio = self.set_volume_control(distance)
				cv2.putText(image, f'Volume: {audio}', (30, 60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)

	def get_camera_capture(self, index=0):
		"""Захватывает изображение с веб-камеры и обрабатывает жесты рук."""
		cap = cv2.VideoCapture(0)

		if not cap.isOpened():
			raise Exception("Ошибка: не удалось открыть камеру.")

		while True:
			ret, image = cap.read()
			if not ret:
				break	
			image = cv2.flip(image, 1)
			imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			
			self.hand_control(image, imageRGB)

			cv2.imshow('Камера', image)

			if cv2.waitKey(1) == 27:
				break

		cap.release()
		cv2.destroyAllWindows()
