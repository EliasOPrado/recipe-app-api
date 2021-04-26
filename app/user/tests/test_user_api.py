from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# create helper
CREATE_USER_URL = reverse('user:create')

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
        payload = {'email': 'test@test.com', 'password': 'hey'}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)