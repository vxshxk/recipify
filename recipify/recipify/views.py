from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect
from .forms import SignupForm, LoginForm, UploadFileForm
from .models import FoodImage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = UploadFileForm()
    
    images = FoodImage.objects.all()
    form = UploadFileForm()
    context = {
        'form': form,
        'images': images,
    }
    return render(request, 'index.html', context)

@login_required
def gallery(request):
    images = FoodImage.objects.all()
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