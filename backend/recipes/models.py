from django.contrib.auth import get_user_model
from django.core import validators
from django.db.models import (CASCADE, CharField, DateTimeField, ForeignKey,
                              ImageField, ManyToManyField, Model,
                              OneToOneField, PositiveSmallIntegerField,
                              TextField, UniqueConstraint)
from django.db.models.functions import Length
from django.db.models.signals import post_save
from django.dispatch import receiver

CharField.register_lookup(Length)
User = get_user_model()


class Ingredient(Model):
    name = CharField(
        'Название ингредиента',
        max_length=200)
    measurement_unit = CharField(
        'Единица измерения ингредиента',
        max_length=200)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ['name']
        constraints = (
            UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_for_ingredient'
            ),
        )

    def __str__(self) -> str:
        return f'{self.name} {self.measurement_unit}'


class Tag(Model):
    name = CharField(
        'Имя',
        max_length=60,
        unique=True)
    color = CharField(
        'Цвет',
        max_length=7,
        unique=True)
    slug = CharField(
        'Ссылка',
        max_length=100,
        unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Recipe(Model):
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='recipe',
        verbose_name='Автор')
    name = CharField(
        'Название рецепта',
        max_length=255)
    image = ImageField(
        'Изображение рецепта',
        upload_to='static/recipe/',
        blank=True,
        null=True)
    text = TextField(
        'Описание рецепта')
    ingredients = ManyToManyField(
        Ingredient,
        through='RecipeIngredient')
    tags = ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes')
    cooking_time = PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[validators.MinValueValidator(
            1, message='Мин. время приготовления 1 минута'), ])
    pub_date = DateTimeField(
        'Дата публикации',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )

    def __str__(self):
        return f'{self.author.email}, {self.name}'


class RecipeIngredient(Model):
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='recipe')
    ingredient = ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        related_name='ingredient')
    amount = PositiveSmallIntegerField(
        default=1,
        validators=(
            validators.MinValueValidator(
                1, message='Мин. количество ингредиентов 1'),
        ),
        verbose_name='Количество',
        help_text='Количество ингредиента в блюде',
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ['-id']
        constraints = [
            UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient')
        ]

        def __str__(self):
            return f"{self.ingredient.name} - {self.amount} шт."


class Subscribe(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='follower',
        verbose_name='Подписчик')
    author = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='following',
        verbose_name='Автор')
    created = DateTimeField(
        'Дата подписки',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-id']
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription')]

    def __str__(self):
        return f'Пользователь {self.user} -> автор {self.author}'


class FavoriteRecipe(Model):
    user = OneToOneField(
        User,
        on_delete=CASCADE,
        null=True,
        related_name='favorite_recipe',
        verbose_name='Пользователь')
    recipe = ManyToManyField(
        Recipe,
        related_name='favorite_recipe',
        verbose_name='Избранный рецепт')

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        list_ = [item['name'] for item in self.recipe.values('name')]
        return f'Пользователь {self.user} добавил {list_} в избранные.'

    @receiver(post_save, sender=User)
    def create_favorite_recipe(sender, instance, created, **kwargs):
        if created:
            favorite_recipe, created = FavoriteRecipe.objects.get_or_create(
                user=instance
            )
            if not created:
                print(f'Рецепт {instance} уже в избранных.')


class ShoppingCart(Model):
    user = OneToOneField(
        User,
        on_delete=CASCADE,
        related_name='shopping_cart',
        null=True,
        verbose_name='Пользователь')
    recipe = ManyToManyField(
        Recipe,
        related_name='shopping_cart',
        verbose_name='Покупка')

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        ordering = ['-id']

    def __str__(self):
        list_ = [item['name'] for item in self.recipe.values('name')]
        return f'Пользователь {self.user} добавил {list_} в покупки.'

    @receiver(post_save, sender=User)
    def create_shopping_cart(sender, instance, created, **kwargs):
        if created and not hasattr(instance, 'shopping_cart'):
            return ShoppingCart.objects.create(user=instance)
