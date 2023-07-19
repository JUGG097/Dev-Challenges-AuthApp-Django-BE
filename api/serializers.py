from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from api.models import CustomUser, RefreshToken


# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "name",
            "email",
            "password",
            "provider",
            "bio",
            "image",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {"password": {"write_only": True}}

        def create(self, validated_data):
            user = CustomUser.objects.create_user(
                email=validated_data["email"],
                password=validated_data["password"],
                name=validated_data["name"],
                bio=validated_data["bio"],
                image=validated_data["image"],
            )
            return user


# RefreshToken serializer
class RefreshTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefreshToken
        fields = "__all__"

        def create(self, validated_data):
            # user_id = self.context["request"].user.id
            refreshToken = RefreshToken.objects.create(
                user=validated_data["user_id"],
                token=validated_data["token"],
                expiry_date=validated_data["expiry_date"],
            )
            return refreshToken
