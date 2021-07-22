from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, mixins
from .serializers import TagSerializer, IngredientSerializer
from core.models import Tag, Ingredient


# Create your views here.

class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """ Manage tags in database """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        """ Return objects for the current authenticated user only """
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """ Create a new tag """
        serializer.save(user=self.request.user)


class IngredientViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin):
    """ Manage Ingredients in database """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()

    def get_queryset(self):
        """ Return objects for the current authenticated user only """
        return self.queryset.filter(user=self.request.user).order_by('-name')
