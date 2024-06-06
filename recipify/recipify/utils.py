import util_functions.image_formatter_fun as im
import util_functions.gemini_call_fun as gm

def image_formatter(img):
    return im.imageFormatter(img)

def getRecipeList(ingredients):
    return gm.getRecipes(ingredients)



