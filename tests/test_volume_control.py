import unittest
import sys
import os

sys.path.append(os.path.abspath('..'))

from volume_control import VolumeControl


class TestVolumeControl(unittest.TestCase):
    def test_set_volume_control_min(self):
        volume_control = VolumeControl()
        set_volume = volume_control.set_volume_control(10)

        self.assertEqual(set_volume, volume_control.min_volume)

    def test_set_volume_control_max(self):
        volume_control = VolumeControl()
        set_volume = volume_control.set_volume_control(170)

        self.assertEqual(set_volume, volume_control.max_volume)

    def test_set_volume_control_mid(self):
        volume_control = VolumeControl()
        expected_volume = (volume_control.max_volume + volume_control.min_volume) // 2
        set_volume = volume_control.set_volume_control(88)

        self.assertEqual(set_volume, expected_volume)


if __name__ == '__main__':
    unittest.main()