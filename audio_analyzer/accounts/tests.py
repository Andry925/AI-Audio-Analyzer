from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class TestAuthentication(APITestCase):

    def setUp(self):
        self.data = {
            "username": "someone11",
            "password": "Superpass@2004",
            "email": "some@gmail.com",
        }
        UserCustomModel = get_user_model()
        self.user = UserCustomModel.objects.create_user(**self.data)

    def test_register_new_user(self):
        data = {
            "username": "someone21",
            "email": "some2@gmail.com",
            "password": "Superpass@2004"
        }
        response = self.client.post(
            reverse('register-user'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_existing_user(self):
        response = self.client.post(
            reverse('register-user'),
            data=self.data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_with_short_password(self):
        data = {
            "username": "someone31",
            "email": "some3@gmail.com",
            "password": "superrrrr"
        }
        response = self.client.post(
            reverse('register-user'),
            data=data,
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login(self):
        response = self.client.post(
            reverse('login-user'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_with_invalid_credentials(self):
        data = {
            "username": "someone11",
            "password": "superpass2232",
            "email": "some@gmail.com",
        }
        response = self.client.post(
            reverse('login-user'), data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout(self):
        response = self.client.post(
            reverse('login-user'), data=self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        response = self.client.post(reverse('logout-user'), format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
