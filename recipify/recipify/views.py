from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from inference_sdk import InferenceHTTPClient
import google.generativeai as genai
from django.core.files.storage import FileSystemStorage
import base64

@login_required
def index(request):
    return render(request, 'index.html')


def loginPage(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', { 'form': form })


def registerPage(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'register.html', { 'form': form })

def logoutPage(request):
    logout(request)
    return redirect('login')

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


def image_upload_view(request):
    if request.method == 'POST' and request.FILES['image-input']:
        image = request.FILES['image-input']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_path = fs.path(filename)  

        with open(file_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

        result = CLIENT.infer(img_base64, model_id="fridge-object/3")
        ingredients = [prediction['class'] for prediction in result['predictions']]
        recipe = getRecipeList(ingredients)

        return render(request, 'index.html', {'recipe': recipe, 'uploaded_file_url': fs.url(filename)})

    return render(request, 'index.html')