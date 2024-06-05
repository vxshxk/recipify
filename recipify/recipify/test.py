import os
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from .models import FoodImage
from django.core.files.uploadedfile import SimpleUploadedFile

# Tests
class UserTestCase(TestCase):
    def test_user(self):
        username = "adityapandia18@gmail.com"
        password = "iamsogood500"
        user = User(username=username)
        user.set_password(password)
        user.save()
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))

class FoodImageTestCase(TestCase):
    def test_image(self):
        newImage = FoodImage()
        image_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'test_image.jpg')
        newImage.image = SimpleUploadedFile(name="test_image.jpg",
                                            content=open(image_path, "rb").read(),
                                            content_type='image/jpeg')
        newImage.save()
        self.assertEqual(FoodImage.objects.count(), 1)