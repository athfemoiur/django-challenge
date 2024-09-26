from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import SignupSerializer, LoginSerializer


def get_token_for_user(user) -> Token:
    token, _ = Token.objects.get_or_create(user=user)
    return token


class SignUpView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_token_for_user(user)
        return Response({
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_400_BAD_REQUEST)

        token = get_token_for_user(user)
        return Response({
            'token': token.key
        }, status=status.HTTP_200_OK)
