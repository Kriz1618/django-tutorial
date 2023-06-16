from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['userId'] = self.user.id
        data['access_token_expiration'] = datetime.now(
        ) + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        data['refresh_token_expiration'] = datetime.now(
        ) + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        return data


class TokenPairSerializer(serializers.Serializer):
    refresh = serializers.SerializerMethodField()
    access = serializers.SerializerMethodField()

    def get_refresh(self, obj):
        return str(obj['refresh'])

    def get_access(self, obj):
        return str(obj['access'])

    def validate(self, attrs):
        try:
            refresh_token = RefreshToken(attrs['refresh'])
            data = {'access': str(refresh_token.access_token),
                    'refresh': str(refresh_token)}
        except Exception as e:
            raise serializers.ValidationError(str(e))
        return data
