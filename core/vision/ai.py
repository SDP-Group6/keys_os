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
    # print("Results", results)
    
    keyboards_data = {}
    
    for result in results:
        if result['label'] == 'keyboard':
            
            keyboard_bounding_box = result['box'] 
            
            # print("Keyboard bounding box", keyboard_bounding_box)
            
            if keyboard_bounding_box is None:
                raise ValueError("No keyboard bounding box found.")
            
            image_height, image_width = image.shape[:2]
            
            # print("Image height", image_height)
            # print("Image width", image_width)

            xmin = keyboard_bounding_box['xmin']
            ymin = keyboard_bounding_box['ymin']
            xmax = keyboard_bounding_box['xmax']
            ymax = keyboard_bounding_box['ymax']
            
            if xmin < 0 or xmax >= image_width or ymin < 0 or ymax >= image_height or xmax <= xmin or ymax <= ymin:
                # Region is not fully contained within image boundaries, skip it
                continue

            keyboard_region = image[ymin : ymax, xmin : xmax]

            edges = cv2.Canny(keyboard_region, 100, 200)
            if edges is None or edges.size == 0:
                raise ValueError("Edge detection failed or returned empty results.")
            
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
            
            all_points = []
            
            for contour in contours:
                contour = np.array(contour, dtype=int)
                
                # Ensure contour has at least 2 points before drawing
                if len(contour) >= 2:
                    dx = xmin  # Horizontal translation to move the contour to inside the bounding box
                    dy = ymin  # Vertical translation to move the contour to inside the bounding box
                    
                    # Translate the contour points by (dx, dy)
                    translated_contour = contour + [dx, dy]
                    
                    # Convert the translated contour to a list of points
                    points = [tuple(p) for p in translated_contour[:, 0]]
                    all_points.append(points)
                    
            keyboards_data[len(keyboards_data) + 1] = {
                "keyboard_bounding_box": keyboard_bounding_box,
                "edges": edges,
                "all_points": all_points
            }
                                                                    
    if len(keyboards_data) == 0:
        raise ValueError("No keyboards detected.")
    
    print(keyboards_data[1]["keyboard_bounding_box"])
    
    return keyboards_data