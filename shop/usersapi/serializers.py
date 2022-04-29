from typing import Dict

from rest_framework import serializers
from customer.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'],
                    email=validated_data['email'])
        password = self.validated_data['password']
        password2_ = self.validated_data['password2']
        if password != password2_:
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        user.set_password(password)
        user.save()
        return user


class LoginUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']


class ConformationCodeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')