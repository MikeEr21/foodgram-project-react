from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from recipes.models import (FavoriteRecipe, Ingredient, Recipe, ShoppingCart,
                            Subscribe, Tag)
from api.serializers import (IngredientSerializer, RecipeReadSerializer,
                          RecipeWriteSerializer, SubscribeRecipeSerializer,
                          SubscribeSerializer, TagSerializer, TokenSerializer,
                          UserCreateSerializer, UserListSerializer,
                          UserPasswordSerializer)

User = get_user_model()


class RecipesViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.tag = Tag.objects.create(
            name='Test tag'
        )
        self.ingredient = Ingredient.objects.create(
            name='Test ingredient',
            measurement_unit='test unit'
        )
        self.recipe = Recipe.objects.create(
            name='Test recipe',
            author=self.user,
            cooking_time=60
        )
        self.recipe.ingredients.add(self.ingredient)
        self.recipe.tags.add(self.tag)
        self.url = reverse('api:recipes-list')
        self.client.force_authenticate(self.user)

    def test_create_recipe(self):
        payload = {
            'name': 'New recipe',
            'cooking_time': 30,
            'ingredients': [self.ingredient.id],
            'tags': [self.tag.id],
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=response.data['id'])
        serializer = RecipeWriteSerializer(recipe)
        self.assertEqual(serializer.data, response.data)

    def test_list_recipes(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipes = Recipe.objects.all()
        serializer = RecipeReadSerializer(recipes, many=True)
        self.assertEqual(serializer.data, response.data)

    def test_retrieve_recipe(self):
        url = reverse('api:recipes-detail', args=[self.recipe.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = RecipeReadSerializer(self.recipe)
        self.assertEqual(serializer.data, response.data)

    def test_update_recipe(self):
        url = reverse('api:recipes-detail', args=[self.recipe.id])
        payload = {
            'name': 'Updated recipe',
            'cooking_time': 45,
            'ingredients': [self.ingredient.id],
            'tags': [self.tag.id],
        }
        response = self.client.put(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe = Recipe.objects.get(id=self.recipe.id)
        serializer = RecipeWriteSerializer(recipe)
        self.assertEqual(serializer.data, response.data)

    def test_partial_update_recipe(self):
        url = reverse('api:recipes-detail', args=[self.recipe.id])
        payload = {
            'name': 'Updated recipe'
        }
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        recipe = Recipe.objects.get(id=self.recipe.id)
        serializer = RecipeWriteSerializer(recipe)
        self.assertEqual(serializer.data, response.data)

    def test_delete_recipe(self):
        self.client.force_authenticate(self.user)
        url = reverse('api:recipes-detail', args=[self.recipe.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=self.recipe.id).exists())
