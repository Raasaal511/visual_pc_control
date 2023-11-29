import cv2
import math

import mediapipe as mp


class HandControl:

	def __init__(self):
		self.hands = mp.solutions.hands.Hands(max_num_hands=1)
		self.draw = mp.solutions.drawing_utils

	def get_finger_distance(self, hand_lms, w, h):
		"""Вычисляет расстояние между указательным и большим пальцами."""
		thumb_x, thumb_y = int(hand_lms.landmark[4].x * w), int(hand_lms.landmark[4].y * h)
		index_x, index_y = int(hand_lms.landmark[8].x * w), int(hand_lms.landmark[8].y * h)
		distance = int(math.sqrt((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2))

		return distance


	def hand_volume_control(self, image, imageRGB, volume_control):
		"""Обрабатывает жест руки и управляет громкостью."""
		h, w, _ = image.shape
		results = self.hands.process(imageRGB)

		if results.multi_hand_landmarks:
			for hand_lms in results.multi_hand_landmarks:
				for id, lm in enumerate(hand_lms.landmark):
					h, w, _ = image.shape
					cx, cy = int(lm.x * w), int(lm.y * h)
					cv2.putText(image, f'{id}', (cx, cy), cv2.FONT_HERSHEY_PLAIN,
								1, (255, 0, 255), 1, cv2.LINE_AA)

				distance = self.get_finger_distance(hand_lms, w, h)
				audio = volume_control.set_volume_control(distance)

				cv2.putText(image, f'Distance: {distance}', (30, 30), cv2.FONT_HERSHEY_PLAIN,
							1, (255, 0, 255), 1, cv2.LINE_AA)
				cv2.putText(image, f'Volume: {audio}', (30, 60), cv2.FONT_HERSHEY_PLAIN,
							1, (255, 255, 255), 1, cv2.LINE_AA)
				self.draw.draw_landmarks(image, hand_lms, mp.solutions.hands.HAND_CONNECTIONS)

