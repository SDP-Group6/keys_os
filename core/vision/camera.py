import os
import cv2
import time


class Camera:
    def __init__(self):
        #Initialize the camera once to avoid reinitialization delays.
        os_type = os.name
        if os_type == "posix":
            print("Using AVFoundation backend for macOS.")
            self.cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
        else:
            self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            raise Exception("Could not open camera.")

        # Set camera properties for speed optimization
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Reduce resolution
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffering delay

        # Warm-up: Capture a few frames before the first photo
        for _ in range(5):
            self.cap.read()
            time.sleep(0.05)  # Allow auto-adjustments

    def take_photo(self, path):
        """Capture and save a photo to the given path."""
        if os.path.exists(path):
            os.remove(path)  # Delete existing file

        ret, frame = self.cap.read()
        if ret:
            cv2.imwrite(path, frame)
            print(f"Image saved successfully: {path}")
        else:
            print("Error: Failed to capture image.")

    def close(self):
        """Release the camera resources."""
        self.cap.release()
        cv2.destroyAllWindows()
        print("Camera released.")