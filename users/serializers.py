from datetime import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["userId"] = self.user.id
        data["access_token_expiration"] = (
            datetime.now() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
        )
        data["refresh_token_expiration"] = (
            datetime.now() + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
        )
        return data


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        refresh_token = data["refresh"]
        if not refresh_token:
            raise serializers.ValidationError("No refresh token was sent")

        try:
            token = RefreshToken(refresh_token)
            jti = token["jti"]
            outstanding_token = OutstandingToken.objects.get(token=jti)
            outstanding_token.blacklist()
        except OutstandingToken.DoesNotExist:
            pass
        except Exception as e:
            raise serializers.ValidationError("Invalid refresh token")

        return {"access": str(token.access_token), "refresh": str(token)}
