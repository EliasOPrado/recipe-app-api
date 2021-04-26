from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# create helper
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserTests(TestCase):
    """ Test user API (public) """

    def SetUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Test create valid user success """
        payload = {
            'email': 'test@test.com',
            'password': '@test123',
            'name': 'test name'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        # encrition and password should not be in
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """ Test create an user already exists fail """
        payload = {'email': 'test@test.com', 'password': '@test123'}
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_and_email_exists(self):
        """ Test that password must have more than 5 characters """
        payload = {'email': 'test@test.com', 'password': 'hey', 'name': 'test'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test that a token is created for user """
        payload = {'email': 'test@test.com', 'password':'test123'}
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """ Test that token is not created if invalid credentials are giving """
        create_user(email='test@email.com', password='test123')
        payload = {'email':'test@email.com', 'password':'wrong'}
        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """ Test token not created if user dont exist """
        # not create_user()
        payload = {'email': 'test@email.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Test that email and/or password are required """
        payload = {'email': 'just', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
