from core.vision.ai import predict_image
from core.vision.camera import take_photo
from core.vision.utils import draw_bounding_boxes_on_image

# The path where we will save temporary images
path = "tmp/image.jpg"


def main():

    # Take a photo
    take_photo(path)

    # Predict the image
    predictions = predict_image(path)

    # Draw bounding boxes on the image
    draw_bounding_boxes_on_image(path, predictions)


if __name__ == "__main__":
    main()
