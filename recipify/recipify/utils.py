import re
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageEnhance
from inference_sdk import InferenceHTTPClient
import google.generativeai as genai



def image_formatter(img):
    if img is None:
        raise ValueError("Image not found or cannot be opened.")
    
    # Apply sharpening using PIL
    proc = ImageEnhance.Sharpness(img)
    proc = proc.enhance(2)
    
    # Apply Contrast enhancement
    proc = ImageEnhance.Contrast(proc)
    proc = proc.enhance(0.3)
    
    # Convert the image into a numpy array
    proc = np.array(proc)
    
    # Apply sharpening kernel
    sharpenerKernel = np.array([[-1, -1, -1,-1,-1],[-1,  2,2,2,-1],[-1, 2, 2,2,-1],[-1, 2,2,2,-1],[-1, -1, -1,-1,-1],])
    proc = cv2.filter2D(proc, -1, sharpenerKernel)

    
    # Convert the image to a numpy array
    proc = np.array(proc)
    
    # Resize the image
    proc = cv2.resize(proc, (640,640))
    
    # Print the shape of the image
    print("Image shape:")
    print(proc.shape)
    print("Image matrix:")
    print(proc)
    
    return proc


# def parse_recipe(recipe_text):
#     # Extracting sections from the recipe text
#     parts = recipe_text.split('**')

#     title = parts[1].strip() if len(parts) > 1 else 'Recipe'
#     ingredients_start = parts.index('Ingredients:') + 1 if 'Ingredients:' in parts else None
#     ingredients_end = parts.index('Instructions:') if 'Instructions:' in parts else None
#     ingredients = parts[ingredients_start].strip() if ingredients_start and ingredients_end else ''
#     instructions_start = ingredients_end + 1 if ingredients_end else None
#     instructions_end = parts.index('Tips:') if 'Tips:' in parts else None
#     instructions = parts[instructions_start].strip() if instructions_start and instructions_end else ''
#     tips_start = instructions_end + 1 if instructions_end else None
#     tips = parts[tips_start].strip() if tips_start else ''

#     return {
#         'title': title,
#         'ingredients': ingredients,
#         'instructions': instructions,
#         'tips': tips
#     }


CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="DhYhkBrtp1M7KLVSxqPZ"
)

genai.configure(api_key='AIzaSyCs_q7nIoDNyST3L8A8c_kBb2Tkd9OhJpk')

def getRecipeList(ingredients):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )

    response = model.generate_content("Give me the list of dishes and step by step recipe of how I can make using the following items: " + str(ingredients))
    return response.text

def extract_recipes(text):
    title = text.split('\n')[1].strip()
    
    recipe_pattern = r'\*\*Recipe \d+: .*?\*\*.*?(?=(?:\*\*Recipe \d+:)|$)'
    recipes = re.findall(recipe_pattern, text, re.DOTALL)
    
    recipe_list = []
    for recipe in recipes:
        recipe_dict = {}
        
        # Extracting recipe name
        name_pattern = r'\*\*Recipe \d+: (.*?)\*\*'
        recipe_name = re.findall(name_pattern, recipe)[0]
        recipe_dict['title'] = recipe_name.strip()
        
        # Extracting yields and prep time
        yields_pattern = r'\* \*\*Yields:\*\* (.*?)\n'
        prep_time_pattern = r'\* \*\*Prep Time:\*\* (.*?)\n'
        
        yields = re.findall(yields_pattern, recipe)
        prep_time = re.findall(prep_time_pattern, recipe)
        
        recipe_dict['yields'] = yields[0].strip() if yields else ''
        recipe_dict['prep_time'] = prep_time[0].strip() if prep_time else ''
        
        # Extracting ingredients
        ingredients_pattern = r'\*\*Ingredients:\*\*(.*?)(?=\*\*Instructions:|\*\*Dressing:)'
        ingredients = re.findall(ingredients_pattern, recipe, re.DOTALL)
        if ingredients:
            ingredients_list = [i.strip() for i in ingredients[0].split('\n') if i.strip() and not i.startswith('* **')]
            recipe_dict['ingredients'] = ingredients_list
        
        # Extracting instructions
        instructions_pattern = r'\*\*Instructions:\*\*(.*?)(?=(\*\*|$))'
        instructions = re.findall(instructions_pattern, recipe, re.DOTALL)
        if instructions:
            instructions_list = [i.strip() for i in instructions[0][0].split('\n') if i.strip()]
            recipe_dict['instructions'] = instructions_list
        
        recipe_list.append(recipe_dict)
    
    return title, recipe_list

