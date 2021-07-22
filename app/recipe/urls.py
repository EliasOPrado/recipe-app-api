from django.urls import path, include
from rest_framework import routers
from recipe import views

router = routers.DefaultRouter()
router.register('tags', views.TagViewSet, basename='tag')
router.register('ingredients', views.IngredientViewSet, basename='ingredients')

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]