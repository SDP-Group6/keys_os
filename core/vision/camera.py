import os

import cv2

def take_photo(path):

    # Delete the path is it already exists
    if os.path.exists(path):
        os.remove(path)

    # Initialize the webcam (0 is the default camera)

    # Get the type of operating system
    os_type = os.name

    # Check if we are using mac
    if os_type == "posix":
        print("Using AVFoundation backend for macOS.")
        cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    else:
        cap = cv2.VideoCapture(0)

    # Allow camera to warm up
    if not cap.isOpened():
        print("Error: Could not open camera.")
        raise Exception("Could not open camera.")

    # Capture a single frame
    ret, frame = cap.read()

    if ret:
        # Save the image
        cv2.imwrite(path, frame)
        print("Image saved successfully.")

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
