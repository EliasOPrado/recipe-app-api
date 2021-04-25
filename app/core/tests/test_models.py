from django.test import TestCase
from django.contrib.auth import get_user_model

"""
The get_user_model() and create_user() are mainly used
in the main User model to greate and get users
"""


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """ test creating a new user with an email is successful """
        email = "email@email.com"
        password = "@testpassword"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))


    def test_new_user_email_normalized(self):
        """ test the email of a new user is normalized """
        email = 'test@ELIASPRADO.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ test creating user with no email rasing error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """ test creating new superuser """
        user = get_user_model().objects.create_superuser('test123@test.com',
                                                         'test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
