import json

from PIL import Image, ImageDraw, ImageFont

from core.const import STANDARD_KEYBOARD_LENGTH_MM, \
    STANDARD_KEYBOARD_BREADTH_MM, STANDARD_KEYBOARD_HEIGHT_MM, \
    CAMERA_PROPERTIES_MM

def draw_bounding_boxes_on_image(image_path='/Input', predictions_json, output_path='tmp/all_boxes.jpeg', min_score=0.5):
    """
    Draws bounding boxes on the image based on predictions in the response JSON.

    Args:
        image_path (str): Path to the input image.
        predictions_json (str): JSON string containing predictions.
        output_path (str): Path to save the output image.
        min_score (float): Minimum confidence score to consider a prediction.
    """

    # If the output path is not provided, save the image in the same directory
    if output_path is None:
        output_path = image_path.replace(".jpg", "_output.jpg")

    # Load the image
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Load a font for the labels (adjust path as needed)
    try:
        font = ImageFont.truetype("arial.ttf", size=18)
    except IOError:
        font = ImageFont.load_default()

    if isinstance(predictions_json, str):
        # Parse the JSON response
        data = json.loads(predictions_json)
    else:
        data = predictions_json

    predictions = data.get("predictions", {}).get("result", [])

    for pred in predictions:
        score = pred.get("score", 0)
        label = pred.get("label", "")
        box = pred.get("box", {})

        if score >= min_score:
            xmin, ymin, xmax, ymax = box["xmin"], box["ymin"], box["xmax"], box["ymax"]

            # Draw the bounding box
            draw.rectangle([(xmin, ymin), (xmax, ymax)], outline="red", width=3)

            # Draw the label with the score
            label_text = f"{label} ({score:.2f})"
            text_width = font.getlength(label_text)
            text_height = font.getbbox(label_text)[3]  # get the height of the text
            text_size = (text_width, text_height)
            text_background = [(xmin, ymin - text_size[1]), (xmin + text_size[0], ymin)]
            draw.rectangle(text_background, fill="red")
            draw.text((xmin, ymin - text_size[1]), label_text, fill="white", font=font)

    # Save the image with bounding boxes
    image.save(output_path)
    print(f"Saved output image to {output_path}")
    
def draw_keyboard_bounding_box_on_image(image_path, keyboards_data, output_path='tmp/keyboard_box.jpeg'):
    # Load the original image
    image = Image.open(image_path)

    image_size = image.size  # (width, height)

    # Create a new black image with the same size as the original image
    white_image = Image.new("RGB", image_size, "white")

    # Create a drawing context on the black image
    draw_white = ImageDraw.Draw(white_image)
    
    # print("Keyboards data", keyboards_data.keys())
    
    for keyboard_id, keyboard_data in keyboards_data.items():
        keyboard_bounding_box = keyboard_data['keyboard_bounding_box']
        all_points = keyboard_data['all_points']
        
        # Get bounding box coordinates
        x = keyboard_bounding_box['xmin']
        y = keyboard_bounding_box['ymin']
        w = keyboard_bounding_box['xmax'] - keyboard_bounding_box['xmin']
        h = keyboard_bounding_box['ymax'] - keyboard_bounding_box['ymin']

        # Draw the bounding box on the black image
        draw_white.rectangle([x, y, x + w, y + h], outline="blue", width=3)

        # Iterate over contours and draw them on the black image
        for points in all_points:
            # Draw the translated contours on the black image
            draw_white.polygon(points, outline="red", width=3)
            
    # Ensure output_path is a valid string
    if not isinstance(output_path, str):
        raise ValueError(f"Invalid output path type: {type(output_path)}, value: {output_path}")

    # Save the image
    white_image.save(output_path)
    print(f"Saved keyboard bounding box image to {output_path}")
    
def estimate_distance_from_camera(keyboard_bounding_box):
    
    # Get the bounding box coordinates
    xmin = keyboard_bounding_box['xmin']
    ymin = keyboard_bounding_box['ymin']
    xmax = keyboard_bounding_box['xmax']
    ymax = keyboard_bounding_box['ymax']
    
    # Get the image width and height
    image_keyboard_width = xmax - xmin
    image_keyboard_height = ymax - ymin
    
    # Calculate the distance from the camera
    focal_length = CAMERA_PROPERTIES_MM['focal_length']
    pixel_size = CAMERA_PROPERTIES_MM['pixel_size']
    
    distance = (focal_length * STANDARD_KEYBOARD_LENGTH_MM / (image_keyboard_width * pixel_size),
                focal_length * STANDARD_KEYBOARD_BREADTH_MM / (image_keyboard_height * pixel_size))
    
    print(f"Estimated distance from camera: ({distance[0]:.2f} mm, {distance[1]:.2f} mm)")
    return distance


def calculate_performance(TP=1, TN=1, FP=1, FN=1):

    #Prints a measurement of model's performance
    accuracy=(TP+TN)/(TP+TN+FN+FP)
    precision=TP/(TP+FP)
    recall=TP/(TP+FN)
    F1 = 2*(precision*recall/(precision+recall))

    print(accuracy, precision, recall, F1)
