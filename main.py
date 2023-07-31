import cv2

from capture import HandGestureAudioControl



def main():
    hand_gesture_audio_control = HandGestureAudioControl()

    hand_gesture_audio_control.get_camera_capture()
    

if __name__ == "__main__":
    main()