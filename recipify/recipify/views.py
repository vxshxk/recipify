from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from .forms import SignupForm, LoginForm
from .models import FoodImage
from .models import Recipe
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from inference_sdk import InferenceHTTPClient
from django.core.files.storage import FileSystemStorage
import base64
from .util_functions.gemini_call_fun import getRecipes
from .util_functions.json_parser import parseRecipes
from .util_functions.json_parser import parseIngredients
from.util_functions.gemini_call_fun import getIngredients
from.util_functions.image_generation import getDishImage
from.util_functions.image_generation import add_base64_padding
from.util_functions.image_generation import decode_base64_to_image

import logging
from PIL import Image


# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="DhYhkBrtp1M7KLVSxqPZ"
)

def index(request):
    return render(request, 'index.html')

@login_required
def gallery(request):
    images = FoodImage.objects.filter(user=request.user)
    context = {
        'images': images,
    }
    return render(request, 'gallery.html', context)

def loginPage(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                messages.success(request, "Logged in successfully!")
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Incorrect username or password!")
                return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = LoginForm()
    return render(request, 'login.html', { 'form': form })

def contact(request):
    return render(request,'contact.html')

def registerPage(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in")
            return redirect('login')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = SignupForm()
    return render(request, 'register.html', { 'form': form })

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required
def image_upload_view(request):
    if request.method == 'POST' and 'image-input' in request.FILES:
        image = request.FILES['image-input']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_path = fs.path(filename)
        img = Image.open(file_path)
        result = getIngredients(img)
        ingredients = parseIngredients(result)
        if ingredients:
            recipe_text = getRecipes(ingredients)
            # Get parsed text from the JSON response
            nRecipes, dishNames, ingredLists, recipeLists, nutrients_present, nutrients_absent = parseRecipes(recipe_text)  
            # Save the image to the FoodImage model
            recipes = []
            food_image = FoodImage(image=filename, user=request.user)
            food_image.save()
            for i in range(nRecipes):
                recipe = Recipe(name=dishNames[i],
                                      ingredients=ingredLists[i],
                                      method=recipeLists[i],
                                      nutrients_present=nutrients_present[i],
                                      nutrients_absent=nutrients_absent[i],
                                      image=food_image,
                                      )
                recipes.append(recipe)
                recipe.save()
                
            # Load parsed text into context dictionary to display on page
            context = {
                'uploaded_file_url': fs.url(filename),
                'recipe_len' : nRecipes,
                'recipes': recipes
            }
            return render(request, 'upload.html', context)
        else:
            error_message = "Failed to retrieve recipes."
            return render(request, 'upload.html', {'error_message': error_message})
    else:
        error_message = "No image file uploaded."
        return render(request, 'upload.html', {'error_message': error_message})

def show_recipe(request, id):

    recipe = get_object_or_404(Recipe, id=id)
    recipeName = recipe.name
    ingredients = recipe.ingredients.replace("[", "").replace("]", "").replace("'", "").split(',')
    steps = recipe.method.split("',")
    steps = [clean(step) for step in steps]
    nutri_present = recipe.nutrients_present.split("',")
    nutri_present = [clean(nutri) for nutri in nutri_present]
    nutri_absent = recipe.nutrients_absent.split("',")
    nutri_absent = [clean(nutri) for nutri in nutri_absent]
    try: 
        img = getDishImage(recipeName)
    except: 
        img = recipe.image
        
    context = {
        "ingredients": ingredients,
        "recipeName":recipeName,
        "steps": steps,
        "nutri_present": nutri_present,
        "nutri_absent": nutri_absent,
        "foodimg": img,

    }
    return render(request, 'show.html', context)

def clean(item):
    filter_chars = ["'", "[", "]"]
    for char in filter_chars:
        item = item.replace(char, "")

    return item.capitalize()


def pick_recipe(request, img_id):
    image = get_object_or_404(FoodImage, id=img_id)
    recipes = Recipe.objects.filter(image=image)
    context = {
        "recipes": recipes
    }

    return render(request, 'pick.html', context)

def delete_recipe(request, id):
    recipe = get_object_or_404(Recipe, id=id)
    img = recipe.image
    recipe.delete()

    associated_recipes = img.recipe_set.all()
    if not associated_recipes:
        img.delete()
        return redirect(reverse('gallery'))

    return redirect(reverse('pick_recipe', args=[img.id]))

