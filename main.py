import cv2

from capture import Capture



def main():
    capture = Capture()

    capture.get_camera_capture()
    

if __name__ == "__main__":
    main()