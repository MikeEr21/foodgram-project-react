from django.test import TestCase

from recipes.models import (FavoriteRecipe, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Subscribe, Tag,
                            User)


class IngredientModelTests(TestCase):
    def test_str_representation(self):
        ingredient = Ingredient.objects.create(
            name='Test Ingredient',
            measurement_unit='Test Unit'
        )
        self.assertEqual(str(ingredient), 'Test Ingredient, Test Unit.')


class TagModelTests(TestCase):
    def test_str_representation(self):
        tag = Tag.objects.create(
            name='Test Tag',
            color='#000000',
            slug='test-tag'
        )
        self.assertEqual(str(tag), 'Test Tag')


class RecipeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_str_representation(self):
        recipe = Recipe.objects.create(
            author=self.user,
            name='Test Recipe',
            text='Test Text',
            cooking_time=5,
        )
        self.assertEqual(str(recipe), f'{self.user.email}, Test Recipe')


class SubscribeModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='testuser1@example.com',
            password='testpassword1'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='testuser2@example.com',
            password='testpassword2'
        )

    def test_str_representation(self):
        subscribe = Subscribe.objects.create(
            user=self.user1,
            author=self.user2
        )
        self.assertEqual(
            str(subscribe),
            f'Пользователь {self.user1} -> автор {self.user2}'
        )


class FavoriteRecipeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            name='Test Recipe',
            text='Test Text',
            cooking_time=5,
        )

    def test_str_representation(self):
        favorite_recipe = FavoriteRecipe.objects.get(user=self.user)
        favorite_recipe.recipe.add(self.recipe)
        self.assertEqual(
            str(favorite_recipe),
            f'Пользователь {self.user} добавил [\'Test Recipe\'] в избранные.'
        )


class ShoppingCartModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            name='Test Recipe',
            text='Test Text',
            cooking_time=5,
        )
        try:
            self.shopping_cart = ShoppingCart.objects.get(user=self.user)
        except ShoppingCart.DoesNotExist:
            self.shopping_cart = ShoppingCart.objects.create(user=self.user)

        self.shopping_cart.recipe.add(self.recipe)

    def test_str_representation(self):
        self.assertEqual(
            str(self.shopping_cart),
            f'Пользователь {self.user} добавил [\'Test Recipe\'] в покупки.'
        )


class RecipeIngredientModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ingredient = Ingredient.objects.create(name='Тестовый ингредиент')
        cls.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
        cls.recipe = Recipe.objects.create(
            name='Тестовый рецепт',
            author=cls.user,
            text='Тестовый текст',
            cooking_time=10
        )
        cls.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=cls.recipe, ingredient=cls.ingredient, amount=2)

    def test_str_representation(self):
        expected = 'Тестовый ингредиент - 2 шт.'
        self.assertEqual(str(self.recipe_ingredient), expected)

    def test_verbose_name(self):
        self.assertEqual(
            RecipeIngredient._meta.verbose_name,
            'Количество ингредиента'
        )
        self.assertEqual(
            RecipeIngredient._meta.verbose_name_plural,
            'Количество ингредиентов'
        )

    def test_help_text(self):
        expected = 'Количество ингредиента в блюде'
        self.assertEqual(
            RecipeIngredient._meta.get_field('amount').help_text, expected
        )

    def test_unique_constraint(self):
        with self.assertRaises(Exception):
            RecipeIngredient.objects.create(
                recipe=self.recipe, ingredient=self.ingredient, amount=3
            )
