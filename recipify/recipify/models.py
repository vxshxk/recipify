from django.db import models


class FoodImage(models.Model):
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.id)


class Recipe(models.Model):
    name = models.CharField(max_length=250)
    ingredients = models.TextField()
    method = models.TextField()
