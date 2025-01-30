import json

from PIL import Image, ImageDraw, ImageFont


def draw_bounding_boxes_on_image(image_path, predictions_json, output_path=None, min_score=0.5):
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
            text_size = draw.textsize(label_text, font=font)
            text_background = [(xmin, ymin - text_size[1]), (xmin + text_size[0], ymin)]
            draw.rectangle(text_background, fill="red")
            draw.text((xmin, ymin - text_size[1]), label_text, fill="white", font=font)

    # Save the image with bounding boxes
    image.save(output_path)
    print(f"Saved output image to {output_path}")