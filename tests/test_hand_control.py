import unittest
import sys
import os
from unittest.mock import MagicMock

sys.path.append(os.path.abspath('..'))

from hand_control import HandControl


class TestHandControl(unittest.TestCase):
    def test_get_finger_distance(self):
        hand_control = HandControl()

        hand_lms = MagicMock()
        hand_lms.landmark = [MagicMock() for _ in range(21)]  # Создаем мок-объект с ландмарками руки

        for landmark_mock in hand_lms.landmark:
            landmark_mock.x = 0.0
            landmark_mock.y = 0.0

        distance = hand_control.get_finger_distance(hand_lms, 100, 100)  # Предположим размеры изображения 100x100
        self.assertEqual(distance, 0)  # Проверяем ожидаемое расстояние


if __name__ == "__main__":
    unittest.main()