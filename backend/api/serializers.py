from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_base64.fields import Base64ImageField
from recipes.models import Ingredient, Recipe, RecipeIngredient, Subscribe, Tag
from rest_framework import serializers
from users.serializers import RecipeUserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = (
            'name',
            'measurement_unit'
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class IngredientsEditSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'amount'
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        max_length=None,
        use_url=True)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all())
    ingredients = IngredientsEditSerializer(
        many=True)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)

    def validate(self, data):
        ingredients = data['ingredients']
        ingredient_list = []
        for items in ingredients:
            ingredient = get_object_or_404(
                Ingredient, id=items['id'])
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'Ингредиент должен быть уникальным!'
                )
            if int(items['amount']) <= 0:
                raise serializers.ValidationError(
                    {'amount': 'Количество ингредиента должно быть больше 0!'}
                )
            ingredient_list.append(ingredient)
        tags = data['tags']
        if not tags:
            raise serializers.ValidationError(
                'Нужен хотя бы один тег для рецепта!')
        for tag_name in tags:
            if not Tag.objects.filter(name=tag_name).exists():
                raise serializers.ValidationError(
                    f'Тега {tag_name} не существует!')
        return data

    def validate_cooking_time(self, cooking_time):
        if int(cooking_time) < 1:
            raise serializers.ValidationError(
                'Время приготовления >= 1!'
            )
        return cooking_time

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        if 'tags' in validated_data:
            instance.tags.set(
                validated_data.pop('tags'))
        return super().update(
            instance, validated_data)

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data


class RecipeReadSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializer(
        many=True,
        read_only=True)
    author = RecipeUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = RecipeIngredientSerializer(
        many=True,
        required=True,
        source='recipe'
    )
    is_favorited = serializers.BooleanField(
        read_only=True
    )
    is_in_shopping_cart = serializers.BooleanField(
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = '__all__'


class SubscribeRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(
        source='author.id'
    )
    email = serializers.EmailField(
        source='author.email'
    )
    username = serializers.CharField(
        source='author.username'
    )
    first_name = serializers.CharField(
        source='author.first_name'
    )
    last_name = serializers.CharField(
        source='author.last_name'
    )
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.BooleanField(
        read_only=True
    )
    recipes_count = serializers.IntegerField(
        read_only=True
    )

    class Meta:
        model = Subscribe
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
            'is_self',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscriptions.filter(author=obj).exists()

    def get_is_self(self, obj):
        user = self.context.get('request').user
        return user == obj

    # def validate(self, validated_data):
    #     author_data = validated_data.pop('author')
    #     author = User.objects.create(**author_data)
    #     request_user = self.context['request'].user
    #     if request_user == author:
    #         raise serializers.ValidationError(
    #             'Нельзя подписаться на самого себя'
    #         )
    #     return validated_data

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = (
            obj.author.recipe.all()[:int(limit)] if limit
            else obj.author.recipe.all())
        return SubscribeRecipeSerializer(
            recipes,
            many=True
        ).data
