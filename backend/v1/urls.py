from api.views import (AddAndDeleteSubscribe, AddDeleteFavoriteRecipe,
                       AddDeleteShoppingCart, IngredientsViewSet,
                       RecipesViewSet, TagsViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import AuthToken, UsersViewSet, set_password

app_name = 'api'

router = DefaultRouter()
router.register('v1/users', UsersViewSet)
router.register('v1/tags', TagsViewSet)
router.register('v1/ingredients', IngredientsViewSet)
router.register('v1/recipes', RecipesViewSet)


urlpatterns = [
     path(
          'v1/auth/token/login/',
          AuthToken.as_view(),
          name='login'),
     path(
          'v1/users/set_password/',
          set_password,
          name='set_password'),
     path(
          'v1/users/<int:user_id>/subscribe/',
          AddAndDeleteSubscribe.as_view(),
          name='subscribe'),
     path(
          'v1/recipes/<int:recipe_id>/favorite/',
          AddDeleteFavoriteRecipe.as_view(),
          name='favorite_recipe'),
     path(
          'v1/recipes/<int:recipe_id>/shopping_cart/',
          AddDeleteShoppingCart.as_view(),
          name='shopping_cart'),
     path('', include(router.urls)),
     path('', include('djoser.urls')),
     path('v1/auth/', include('djoser.urls.authtoken')),
]
