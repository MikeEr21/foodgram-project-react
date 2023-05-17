import django.contrib.auth.password_validation as validators
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import (ValidationError,
                                                     validate_password)
from rest_framework import serializers

User = get_user_model()
ERR_MSG = 'Не удаётся войти в систему с предоставленными учётными данными.'


class GetIsSubscribedMixin:

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if not user.is_authenticated:
            return False
        return user.follower.filter(author=obj).exists()


class TokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label='Email',
        write_only=True
    )
    password = serializers.CharField(
        label='Пароль',
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label='Токен',
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError(
                    ERR_MSG,
                    code='authorization'
                )
        else:
            msg = 'Необходимо указать "адрес электронной почты" и "пароль".'
            raise serializers.ValidationError(
                msg,
                code='authorization'
            )
        attrs['user'] = user
        return attrs


class UserListSerializer(
        GetIsSubscribedMixin,
        serializers.ModelSerializer
):
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Поле обязательно для заполнения.'
        }
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'Адрес электронной почты обязательно для заполнения.',
            'invalid': 'Введите корректный адрес электронной почты.'
        }
    )
    username = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Имя пользователя обязательно для заполнения.'
        }
    )
    first_name = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Имя обязательно для заполнения.'
        }
    )
    last_name = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Фамилия обязательно для заполнения.'
        }
    )
    password = serializers.CharField(
        required=True,
        error_messages={
            'required': 'Пароль обязательно для заполнения.'
        }
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def validate_password(self, password):
        validators.validate_password(password)
        return password


class UserPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        label='Новый пароль'
    )
    current_password = serializers.CharField(
        label='Текущий пароль'
    )

    def validate_current_password(self, current_password):
        user = self.context['request'].user
        if not authenticate(
                username=user.email,
                password=current_password):
            raise serializers.ValidationError(
                ERR_MSG, code='authorization'
            )
        return current_password

    def validate_new_password(self, new_password):
        try:
            validate_password(new_password)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages[0])

        return new_password

    def create(self, validated_data):
        user = self.context['request'].user
        password = make_password(
            validated_data.get('new_password')
        )
        user.password = password
        user.save()
        return validated_data


class RecipeUserSerializer(
    GetIsSubscribedMixin,
    serializers.ModelSerializer
):

    is_subscribed = serializers.SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
