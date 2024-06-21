import google.generativeai as genai
import json
import traceback
from PIL import Image

genai.configure(api_key='AIzaSyCs_q7nIoDNyST3L8A8c_kBb2Tkd9OhJpk')

def getIngredients(img):
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }
  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
  ]


  model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
  

  
  try:
    response = model.generate_content([img, "Detect the ingredients in the image and strictly only give the list of food and food ingredients present in the image. Give the output in the json format of having one field list which is a list of ingredients = { ingredient_name: str } with only json part and without the text and quotes before or after, and the 'list' field must be there even if there is no ingredient detected in the image."])
    start_index = response.text.find('{')
    end_index = response.text.rfind('}') + 1
    jsonresponse = json.loads(response.text[start_index:end_index])
  except:
    jsonresponse = {
    "list": []
  }
  return jsonresponse


def getRecipes(ingredients):
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }
  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
  ]


  model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
  )
  
  try:
    response = model.generate_content("Give me the list of dishes and step by step recipe of how I can make using the following items: "
                                      +str(ingredients)
                                      + " Give the output in the json of having one field list which is a list of Recipe = { dish_name: str , ingredients_required: numbered list, recipe: bullet list }  with only json part and without the text and quotes before or after, and the 'list' field must be there even if there is only one recipe object")
    
    start_index = response.text.find('{')
    end_index = response.text.rfind('}') + 1
    jsonresponse = json.loads(response.text[start_index:end_index])
  except:
    jsonresponse = {
    "list": [
      {
        "dish_name": "Sorry, some unknown error occured!",
        "ingredients_required": ["Please try again!"],
        "recipe": [" "]
      }
    ]
  }
  return jsonresponse


def getNutrition(recipeName):
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }
  safety_settings = [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
      "category": "HARM_CATEGORY_HATE_SPEECH",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
      "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
      "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
  ]


  model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    safety_settings=safety_settings,
    generation_config=generation_config,
  )
  
  try:
    response = model.generate_content("Can you give me the nutritional breakdown of "+ str(recipeName) + ". It should include all the nutrients available in the meal, and the ones that are not"
                                        + " Give the output in the json format { dish_name: str , nutrients_present: bullet list, nutrients_absent: bullet list } with field names in double quotes and with only json part and without the text and quotes before or after") 
    start_index = response.text.find('{')
    end_index = response.text.rfind('}') + 1
    jsonresponse = json.loads(response.text[start_index:end_index])
    print(response.text)
    
  except Exception as e:
    # print(e)
    # print(traceback.format_exc())
    jsonresponse = {
    "dish_name": "ERROR!",
    "nutrients_present": ["Sorry, some unknown error occured!"],
    "nutrients_absent": ["Please try again!"]
    }
  return jsonresponse

#print(getRecipes(["tomato", "onion", "potato", "soyabean", "soya sauce", "salt", "pepper", "chilli powder", "ginger", "garlic", "coriander", "cumin", "turmeric", "garam masala", "oil"]))
# print(getNutrition("Simple Potato & Onion Curry"))
# img = Image.open('media/photo_2024-06-13_13-18-16_TKUg8Y0.jpg')
# print(getIngredients(img))