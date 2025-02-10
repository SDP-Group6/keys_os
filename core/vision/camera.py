import os
try:
    import cv2
except ImportError:
    pass
import time
try:
    from picamera2 import Picamera2
except ImportError:
    pass


def is_pi_camera_present():
    """Check if a Raspberry Pi Camera is available."""
    try:
        picam2 = Picamera2()
        cameras = picam2.enumerate_cameras()
        return bool(cameras)
    except Exception:
        return False


class Camera:
    def __init__(self):
        """Initialize the camera with fallback from Pi Camera to USB Camera."""
        self.pi_camera = None
        self.usb_camera = None

        if is_pi_camera_present():
            print("Using Raspberry Pi Camera Module.")
            self.pi_camera = Picamera2()
            self.pi_camera.start()
        else:
            print("Pi Camera not detected, falling back to USB Camera.")
            os_type = os.name
            if os_type == "posix":
                print("Using AVFoundation backend for macOS.")
                self.usb_camera = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
            else:
                self.usb_camera = cv2.VideoCapture(0)

            if not self.usb_camera.isOpened():
                print("Error: Could not open USB camera.")
                raise Exception("No available camera detected.")

            # Set camera properties for speed optimization
            self.usb_camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.usb_camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.usb_camera.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffering delay

            # Warm-up: Capture a few frames before the first photo
            for _ in range(5):
                self.usb_camera.read()
                time.sleep(0.05)  # Allow auto-adjustments

    def take_photo(self, path):
        """Capture and save a photo to the given path."""
        if os.path.exists(path):
            os.remove(path)  # Delete existing file

        if self.pi_camera:
            self.pi_camera.capture_file(path)
            print(f"Image saved successfully from Pi Camera: {path}")
        elif self.usb_camera:
            ret, frame = self.usb_camera.read()
            if ret:
                cv2.imwrite(path, frame)
                print(f"Image saved successfully from USB Camera: {path}")
            else:
                print("Error: Failed to capture image.")

    def close(self):
        """Release the camera resources."""
        if self.pi_camera:
            self.pi_camera.stop()
            print("Pi Camera released.")
        if self.usb_camera:
            self.usb_camera.release()
            cv2.destroyAllWindows()
            print("USB Camera released.")