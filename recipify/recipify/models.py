from django.db import models
from django.contrib.auth.models import User

class FoodImage(models.Model):
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)


class Recipe(models.Model):
    name = models.CharField(max_length=250)
    ingredients = models.TextField()
    method = models.TextField()
