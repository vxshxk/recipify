import requests
import json
from PIL import Image
import base64
from io import BytesIO


def add_base64_padding(base64_string):
    missing_padding = len(base64_string) % 4
    if missing_padding:
        base64_string += '=' * (4 - missing_padding)
    return base64_string

def decode_base64_to_image(base64_string):
    base64_string = add_base64_padding(base64_string)
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image

def getDishImage(dishname):
    url = "https://api.serphouse.com/serp/live?q=" + dishname + " image&engine=google_images&lang=en&device=desktop&serp_type=web&loc=Alba,Texas,United States&loc_id=1026201&verbatim=0&gfilter=0&page=1&num_result=10"
    
    payload = {}
    headers = {
        'Authorization': 'Bearer nddeuNFHxu2hxN0wzW8euCXbUOawG25WLnpNFdiggt8q4wPKiWTx8AS9T1Iw'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    ans = json.loads(response.text)
    image_base_64 = ans['results']['results']['inline_images'][0]['image']
    return image_base_64

# Example usage
# dish_image_base64 = getDishImage("Kiwi Salsa")
# print(dish_image_base64)
# image = decode_base64_to_image(dish_image_base64)
# image.show()

