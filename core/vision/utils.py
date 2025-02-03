import cv2
import json
import numpy as np

from PIL import Image, ImageDraw, ImageFont
from skimage import measure

def draw_bounding_boxes_on_image(image_path, predictions_json, output_path='tmp/all_boxes.jpeg', min_score=0.5):
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
    
def draw_keyboard_bounding_box_on_image(image_path, keyboard_bounding_box, edges, output_path='tmp/keyboard_box.jpeg'):
    # Load the original image
    image = Image.open(image_path)
    
    # Ensure edges is a 2D image
    if edges.ndim == 3:
        edges = edges[:, :, 0]

    if edges.dtype != np.uint8:
        edges = edges.astype(np.uint8)

    # Ensure edges is not empty
    if edges.size == 0:
        raise ValueError("No edges to process.")

    # Find contours of the edges
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    image_size = image.size  # (width, height)

    # Create a new black image with the same size as the original image
    black_image = Image.new("RGB", image_size, "black")

    # Create a drawing context on the black image
    draw_black = ImageDraw.Draw(black_image)

    # Get bounding box coordinates
    x = keyboard_bounding_box['xmin']
    y = keyboard_bounding_box['ymin']
    w = keyboard_bounding_box['xmax'] - keyboard_bounding_box['xmin']
    h = keyboard_bounding_box['ymax'] - keyboard_bounding_box['ymin']

    # Draw the bounding box on the black image
    draw_black.rectangle([x, y, x + w, y + h], outline="blue", width=3)

    # Iterate over contours and draw them on the black image
    for contour in contours:
        contour = np.array(contour, dtype=int)
        
        # Ensure contour has at least 2 points before drawing
        if len(contour) >= 2:
            dx = x  # Horizontal translation to move the contour to inside the bounding box
            dy = y  # Vertical translation to move the contour to inside the bounding box
            
            # Translate the contour points by (dx, dy)
            translated_contour = contour + [dx, dy]
            
            # Convert the translated contour to a list of points
            points = [tuple(p) for p in translated_contour[:, 0]]

            # Draw the translated contours on the black image
            draw_black.polygon(points, outline="red", width=3)

    # Ensure output_path is a valid string
    if not isinstance(output_path, str):
        raise ValueError(f"Invalid output path type: {type(output_path)}, value: {output_path}")

    # Save the black image
    black_image.save(output_path)
    print(f"Saved keyboard bounding box image to {output_path}")