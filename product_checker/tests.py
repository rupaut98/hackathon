
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Ingredient

class UserRegistrationTest(TestCase):
    def test_successful_registration(self):
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'password123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_registration_with_missing_fields(self):
        url = reverse('register')
        data = {'username': 'newuser'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

class UserLoginTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.url = reverse('login')

    def test_successful_login(self):
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.json())

    def test_wrong_password(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 400)  # Or whatever status code you return for authentication failure
        self.assertTrue('error' in response.json())


class CheckIngredientsTest(TestCase):

    def setUp(self):
        Ingredient.objects.create(name='Sugar', is_unhealthy=True)
        self.url = reverse('check-ingredients')

    def test_ingredient_unhealthy(self):
        data = {'ingredients': ['Sugar']}
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()[0]['is_unhealthy'])

    def test_ingredient_not_found(self):
        data = {'ingredients': ['UnknownIngredient']}
        response = self.client.post(self.url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()[0]['is_unhealthy'])

