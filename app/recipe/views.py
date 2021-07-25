from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer, RecipeDetailSerializer
from core.models import Tag, Ingredient, Recipe


# Create your views here.

class BaseRecipeAttrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """ Base viewset for user owned recipe attributes """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Return objects for the current authenticated user only """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Create a new object """
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAttrViewSet):
    """ Manage tags in database """
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """ Manage Ingredients in database """
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(viewsets.ModelViewSet):
    """ Manage Recipes in database """
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """ Retrieve the recipes for the authenticated user """
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """ Return appropriated serializer class"""
        if self.action == 'retrieve':
            return RecipeDetailSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """ Create new recipe """
        return serializer.save(user=self.request.user)
