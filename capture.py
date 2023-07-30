import cv2
import math
import mediapipe as mp
import sounddevice as sd
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def set_volume_control(distance):
    """Устанавливает громкость в зависимости от дистанции между пальцами."""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume_range = volume.GetVolumeRange()

    min_volume = volume_range[0]
    max_volume = volume_range[1]
	
    vol = int(np.interp(distance, [10,170], [min_volume, max_volume]))
    
    volume.SetMasterVolumeLevel(vol, None)

    return vol


def get_finger_distance(hand_lms, w, h):
    """Вычисляет расстояние между указательным и большим пальцами."""
    thumb_x, thumb_y = int(hand_lms.landmark[4].x * w), int(hand_lms.landmark[4].y * h)
    index_x, index_y = int(hand_lms.landmark[8].x * w), int(hand_lms.landmark[8].y * h)
    distance = int(math.sqrt((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2))

    return distance


def hand_control(hands, image, imageRGB, draw):
	"""Обрабатывает жест руки и управляет громкостью."""

	results = hands.process(imageRGB)
	h, w, _ = image.shape
	
	if results.multi_hand_landmarks:
		for hand_lms in results.multi_hand_landmarks:
			for id, lm in enumerate(hand_lms.landmark):
				h, w, _ = image.shape
				cx, cy = int(lm.x * w), int(lm.y * h)
				cv2.putText(image, f'{id}', (cx, cy), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1, cv2.LINE_AA)

			distance = get_finger_distance(hand_lms, w, h)
			cv2.putText(image, f'Distance: {distance}', (30, 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1, cv2.LINE_AA)
				
			draw.draw_landmarks(image, hand_lms, mp.solutions.hands.HAND_CONNECTIONS)

			audio = set_volume_control(distance)
			cv2.putText(image, f'Volume: {audio}', (30, 60), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1, cv2.LINE_AA)


def get_camera_capture(index=0):
    """Захватывает изображение с веб-камеры и обрабатывает жесты рук."""
    cap = cv2.VideoCapture(index)

    if not cap.isOpened():
        raise Exception("Ошибка: не удалось открыть камеру.")
    
    hands = mp.solutions.hands.Hands(max_num_hands=1)
    draw = mp.solutions.drawing_utils

    while True:
        ret, image = cap.read()
        if not ret:
            break
        
        image = cv2.flip(image, 1)
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        hand_control(hands, image, imageRGB, draw) # Обпроботывает жесты рук.

        cv2.imshow('Камера', image)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()