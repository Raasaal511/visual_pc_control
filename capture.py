import cv2

from hand_control import HandControl
from volume_control import VolumeControl


class Capture:
	"""
	Обрабатывает жесты рук, определяет расстояние между указательным и большим пальцами,
	и управляет громкостью аудио в зависимости от этого расстояния.
	"""

	def __init__(self):
		self.cap = cv2.VideoCapture(0)

	def get_camera_capture(self):
		"""Захватывает изображение с веб-камеры и обрабатывает жесты рук."""
		hand_control = HandControl()
		volume_control = VolumeControl()

		if not self.cap.isOpened():
			raise ValueError("Ошибка: не удалось открыть камеру.")

		while True:
			ret, image = self.cap.read()
			if not ret:
				break	
			image = cv2.flip(image, 1)
			imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
			
			hand_control.hand_volume_control(image, imageRGB, volume_control)

			cv2.imshow('Камера', image)

			if cv2.waitKey(1) == 27:
				break

		self.cap.release()
		cv2.destroyAllWindows()
