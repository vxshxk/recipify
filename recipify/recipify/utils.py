import image_formatter_fun as im
import gemini_call_fun as gm

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageEnhance

def image_formatter(img):
    return im.imageFormatter(img)

def getRecipeList(ingredients):
    return gm.getRecipes(ingredients)

image_path = 'examples/aaa.jpg'
img = Image.open(image_path)
img_canny = image_formatter(img)

fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].imshow(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
ax[0].set_title('Original Image')
ax[0].axis('off')

ax[1].imshow(img_canny, cmap='gray')
ax[1].set_title('Sharper image')
ax[1].axis('off')

plt.show()

