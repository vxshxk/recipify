from django.contrib import admin
from .models import FoodImage
from .models import Recipe
from .models import DishImage

admin.site.register(FoodImage)
admin.site.register(Recipe)
admin.site.register(DishImage)