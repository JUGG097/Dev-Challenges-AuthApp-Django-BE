from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework import generics, permissions, viewsets
from api.models import CustomUser, RefreshToken
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import AccessToken
import datetime
import pytz
import uuid

from api.serializers import RefreshTokenSerializer, UserSerializer


@api_view(["GET"])
def health_check(request):
    return Response({"success": True}, 200)


class AuthView(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    @action(["post"], detail=True)
    def register_user(self, request):
        # Checks if password meets minimum requirements to be registered
        validate_password(request.data["password"])

        # Hash password before sending to serializer
        request.data["password"] = make_password(request.data["password"])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT token
        return Response(
            {
                "success": True,
                "data": self.get_serializer(user).data,
                "message": "Sign Up Successful",
                "authToken": str(AccessToken.for_user(user)),
            }
        )

    @action(["post"], detail=True)
    def login_user(self, request):
        # Check if user exists
        try:
            user = CustomUser.objects.get(email=request.data.get("email"))
        except:
            return Response(
                {
                    "success": False,
                    "message": "User not found",
                },
                404,
            )

        # Compare passwords
        if not user.check_password(request.data.get("password")):
            return Response(
                {
                    "success": False,
                    "message": "Invalid Credentials",
                },
                400,
            )

        # Generate refresh token and save to table
        expiry_date = datetime.datetime.now() + datetime.timedelta(hours=24)
        refreshTokenSerializer = RefreshTokenSerializer(
            data={
                "user": user.id,
                "token": str(uuid.uuid4()),
                "expiry_date": expiry_date,
            }
        )
        refreshTokenSerializer.is_valid(raise_exception=True)
        refreshToken = refreshTokenSerializer.save()

        return Response(
            {
                "success": True,
                "data": self.get_serializer(user).data,
                "message": "Login Successful",
                "authToken": str(AccessToken.for_user(user)),
                "refreshToken": str(refreshToken),
            }
        )

    @action(["post"], detail=True)
    def refresh_token(self, request):
        # Check if refresh token exists
        try:
            refreshToken = RefreshToken.objects.get(
                token=request.data.get("refreshToken")
            )
        except:
            return Response(
                {
                    "success": False,
                    "message": "Invalid refresh token",
                },
                401,
            )

        # Check if refresh token is valid
        curr_time = datetime.datetime.now()
        # To add offset-aware to timestamp
        curr_time = curr_time.replace(tzinfo=pytz.utc)
        if curr_time > refreshToken.expiry_date:
            return Response(
                {
                    "success": False,
                    "message": "Expired refresh token",
                },
                401,
            )

        # Check if user exists
        try:
            user = CustomUser.objects.get(id=refreshToken.user_id)
        except:
            return Response(
                {
                    "success": False,
                    "message": "User not found",
                },
                404,
            )

        return Response(
            {
                "success": True,
                "authToken": str(AccessToken.for_user(user)),
                "refreshToken": request.data.get("refreshToken"),
            }
        )


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        # Retrieve user information
        try:
            user = CustomUser.objects.get(id=user_id)
        except:
            return Response(
                {
                    "success": False,
                    "message": "User not found",
                },
                404,
            )

        return Response(
            {
                "success": True,
                "data": self.get_serializer(user).data,
            }
        )

    def put(self, request):
        user_id = request.user.id
        # Retrieve user information
        try:
            user = CustomUser.objects.get(id=user_id)
        except:
            return Response(
                {
                    "success": False,
                    "message": "User not found",
                },
                404,
            )

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_user = serializer.save()

        return Response(
            {
                "success": True,
                "data": self.get_serializer(updated_user).data,
            }
        )
