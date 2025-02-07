from core.cleaning.usb import Arduino
from core.vision.ai import predict_image
from core.vision.camera import Camera

# The path where we will save temporary images
path = "tmp/image.jpeg"


def main():
    ard = Arduino("/dev/tty.usbmodem0000011")
    cam = Camera()

    for _ in range(100):

        # Take a photo
        cam.take_photo(path)

        # Predict the image
        prediction_image = predict_image(path)

        # Get the predictions
        prediction = prediction_image["predictions"]
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
