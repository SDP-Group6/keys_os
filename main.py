from core.vision.ai import predict_image
from core.vision.camera import take_photo
from core.vision.utils import draw_bounding_boxes_on_image, draw_keyboard_bounding_box_on_image
from core.vision.ai import extract_keyboard_and_detect_edges

# The path where we will save temporary images
path = "tmp/image.jpeg"


def main():

    # Take a photo
    take_photo(path)

    # Predict the image
    predictions = predict_image(path)

    # Extract the keyboard region and detect edges
    keyboard_bounding_box, edges = extract_keyboard_and_detect_edges(path, predictions)
    
    # Draw bounding boxes on the image
    draw_bounding_boxes_on_image(path, predictions)
    
    draw_keyboard_bounding_box_on_image(path, keyboard_bounding_box, edges)
    
if __name__ == "__main__":
    main()
