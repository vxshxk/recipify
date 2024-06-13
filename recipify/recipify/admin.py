from django.contrib import admin
from .models import FoodImage
from .models import Recipe

admin.site.register(FoodImage)
admin.site.register(Recipe)