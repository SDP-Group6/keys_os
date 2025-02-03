import json
import requests
import cv2
import numpy as np

from core.const import PREDICT_URL

def predict_image(path):

    # Get the image data from the path
    with open(path, "rb") as image_file:
        image_data = image_file.read()

    # The headers for the request
    headers = {
        "Content-Type": "image/jpeg",
    }

    # Make a POST request to the server
    response = requests.post(PREDICT_URL, headers=headers, data=image_data)

    # Check if the request was successful
    if response.status_code != 200:
        raise Exception("The request failed with status code: " + str(response.status_code))

    # Return the response
    return response.json()

def extract_keyboard_and_detect_edges(path, predictions):
    image = cv2.imread(path)
    if image is None:
        raise FileNotFoundError(f"Unable to load image at path: {path}")

    results = predictions['predictions']['result']
    keyboard_bounding_box = None
    for result in results:
        if result['label'] == 'keyboard':
            keyboard_bounding_box = result['box'] 
            break

    if keyboard_bounding_box is None:
        return None

    keyboard_region = image[keyboard_bounding_box['ymin']:keyboard_bounding_box['ymax'],
                            keyboard_bounding_box['xmin']:keyboard_bounding_box['xmax']]
    
    edges = cv2.Canny(keyboard_region, 100, 200)
    if edges is None or edges.size == 0:
        raise ValueError("Edge detection failed or returned empty results.")

    return keyboard_bounding_box, edges