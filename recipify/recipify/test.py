import os
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from .models import FoodImage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.loader import render_to_string
from django.urls import reverse


# Tests
class UserTestCase(TestCase):
    def test_user(self):
        username = "ady"
        password = "iamsogood500"
        user = User(username=username)
        user.set_password(password)
        user.save()
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))


class UserRegistrationTests(TestCase):

    def setUp(self):
        self.initial_user_count = User.objects.count()

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'testUser',
            'password1': 'iamsogood500',
            'password2': 'iamsogood500',
        })

        self.assertEqual(User.objects.count(), self.initial_user_count+1)
        self.assertEqual(User.objects.latest('date_joined').username, 'testUser')
        self.assertRedirects(response, reverse('login'))


class UserLoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testUser2", password="iamsogood500")

    def test_login_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'testUser2',
            'password': 'iamsogood500'
        })
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertRedirects(response, reverse('home'))


class HomePageAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testUser3", password="terimakisushi100")

    def test_home_page_acces(self):
        self.client.login(username="testUser3", password="terimakisushi100")
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'RecipifyAI')


class FoodImageTestCase(TestCase):
    def test_image(self):
        newImage = FoodImage()
        image_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'test_image.jpg')
        newImage.image = SimpleUploadedFile(name="test_image.jpg",
                                            content=open(image_path, "rb").read(),
                                            content_type='image/jpeg')
        newImage.save()
        self.assertEqual(FoodImage.objects.count(), 1)