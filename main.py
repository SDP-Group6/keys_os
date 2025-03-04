from core.cleaning.usb import Arduino
from core.utils.wifi import connect_wifi
from core.vision.ai import predict_image
from core.vision.camera import Camera

# The path where we will save temporary images
ssid = ""
password = ""
path = "tmp/image.jpeg"
usb_serial = "/dev/ttyACM0"


def main():

    # Set up the arduino and camera
    ard = Arduino(usb_serial)
    cam = Camera()

    #Connect to wifi
    success = connect_wifi(ssid, password)

    if not success:
        raise Exception("Failed to connect to wifi")

    for _ in range(100):

        # Take a photo
        cam.take_photo(path)

        # Predict the image
        predictions = predict_image(path)

        # Get the predictions
        prediction = predictions["predictions"]
        result = prediction["result"]

        scores = {}

        for r in result:
            label = r["label"]
            score = r["score"]

            # Check if the label is already in the scores
            if label not in scores or scores[label] is None or scores[label] < score:
                scores[label] = score

        if "keyboard" in scores and scores["keyboard"] > 0.5:
            print("Keyboard Detected!")
            # Set the led to on
            ard.send_cmd("led", 1)
        else:
            print("Keyboard Not Detected!")
            # Set the led to off
            ard.send_cmd("led", 0)


if __name__ == "__main__":
    main()

