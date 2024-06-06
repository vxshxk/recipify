import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageEnhance


def imageFormatter(img):
    if img is None:
        raise ValueError("Image not found or cannot be opened.")
    
    # Apply sharpening using PIL
    # proc = ImageEnhance.Sharpness(img)
    # proc = proc.enhance(2)
    
    # Apply Contrast enhancement
    proc = ImageEnhance.Contrast(img)
    proc = proc.enhance(1.3)
    
    # Convert the image into a numpy array
    proc = np.array(proc)
    
    # Apply sharpening kernel
    for i in range(7):
        sharpenerKernel = np.array([[-1,0,-1], [0,5,0],[-1,0,-1]])
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
