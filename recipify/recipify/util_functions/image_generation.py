import requests
import json
from recipify.settings import UNSPLASH_KEY

# def add_base64_padding(base64_string):
#     missing_padding = len(base64_string) % 4
#     if missing_padding:
#         base64_string += '=' * (4 - missing_padding)
#     return base64_string

# def decode_base64_to_image(base64_string):
#     base64_string = add_base64_padding(base64_string)
#     image_data = base64.b64decode(base64_string)
#     image = Image.open(BytesIO(image_data))
#     return image

def getDishImage(dishname):
    client_ID = UNSPLASH_KEY
    url = "https://api.unsplash.com/search/photos/?client_id=" + client_ID + "&query=" + dishname
    
    
    try:
        response = requests.request("GET", url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        ans = json.loads(response.text)
        image_url = ans['results'][0]['urls']['regular']
        return image_url
    except requests.exceptions.RequestException as e:
        # Handle any requests exceptions (e.g., network issues, invalid responses)
        print(f"An error occurred with the request: {e}")
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors
        print(f"An error occurred while decoding the JSON response: {e}")
    except (KeyError, IndexError) as e:
        # Handle errors related to accessing specific elements in the JSON response
        print(f"An error occurred while accessing the JSON data: {e}")
    except Exception as e:
        # Handle any other unforeseen exceptions
        print(f"An unexpected error occurred: {e}")

    return None

# Test
# img = getDishImage("Kiwi Grill  ")
# print(img)

