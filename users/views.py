from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import (CustomTokenObtainPairSerializer,
                          RefreshTokenSerializer, User, UserSerializer)


class RegisterView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(
            username=username,
            password=password
        )
        if user:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                return Response(login_serializer.validated_data, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class ProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'This is a protected endpoint!'}
        return Response(content)


class RefreshTokenView(TokenRefreshView):
    authentication_classes = [JWTAuthentication]
    serializer_class = RefreshTokenSerializer

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)


class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(username=request.data.get('username', ''))
        if user.exists() and user[0] == request.user:
            RefreshToken.for_user(user.first())
            return Response({'message': 'Session closed successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
