from api.serializers import SubscribeSerializer
from django.contrib.auth import get_user_model
from django.db.models.expressions import Exists, OuterRef, Value
from djoser.views import UserViewSet
from recipes.models import Subscribe
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.serializers import (TokenSerializer, UserListSerializer,
                               UserPasswordSerializer, UserCreateSerializer)

User = get_user_model()


class AuthToken(ObtainAuthToken):
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {'auth_token': token.key},
            status=status.HTTP_201_CREATED
        )


class UsersViewSet(UserViewSet):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method.lower() == 'post':
            return UserCreateSerializer
        return UserListSerializer

    def get_queryset(self):
        return User.objects.annotate(
            is_subscribed=Exists(
                self.request.user.follower.filter(
                    author=OuterRef('id'))
            )
        ).prefetch_related(
                'follower', 'following'
        ) if self.request.user.is_authenticated else User.objects.annotate(
            is_subscribed=Value(False)
        )

    @action(
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        queryset = Subscribe.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages, many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)


# @api_view(['POST'])
# def create_user(request):
#     serializer = UserCreateSerializer(data=request.data)
#     if serializer.is_valid():
#         user = serializer.save()
#         return Response(
#             UserCreateSerializer(user).data,
#             status=status.HTTP_201_CREATED
#         )
#     return Response(
#         serializer.errors,
#         status=status.HTTP_400_BAD_REQUEST
#     )


@api_view(['post'])
def set_password(request):
    serializer = UserPasswordSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'message': 'Пароль изменён!'},
            status=status.HTTP_201_CREATED
        )
    return Response(
        {'error': 'Введите верные данные!'},
        status=status.HTTP_400_BAD_REQUEST
    )
