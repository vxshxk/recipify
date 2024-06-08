from recipify.util_functions.image_formatter_fun import imageFormatter
from recipify.util_functions.gemini_call_fun import getRecipes

import cv2
import matplotlib.pyplot as plt
from PIL import Image,ImageEnhance

def image_formatter(img):
    return imageFormatter(img)

def getRecipeList(ingredients):
    return getRecipes(ingredients)

# def add_new_lines(input_string):
#     # Split the input string by '\n' and join them with actual new line characters
#     return '\n'.join(input_string.split('\n'))