import cv2

def take_photo(path):

    # Initialize the webcam (0 is the default camera)
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
