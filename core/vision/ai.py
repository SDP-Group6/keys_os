import requests

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
