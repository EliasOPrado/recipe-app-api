from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

"""
The get_user_model() and create_user() are mainly used
in the main User model to create and get users
"""


def sample_user(email='sample@email.com', password='testpass'):
    """ create sample user """
    return get_user_model().objects.create_user(email, password)


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

    def test_tag_str(self):
        """ test the tag string representation """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='vegan'
        )
        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """ test the ingredient strng representation """
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )
        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """ test the ingredient strng representation """
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='the title',
            time_minutes=5,
            price=5.00
        )
        self.assertEqual(str(recipe), recipe.title)
