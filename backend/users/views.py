from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from .serializers import (UserRegistrationSerializer, UserLoginSerializer,
                          EditUserSerializer, ChangeUserPasswordSerializer)


class UserRegistrationAPIView(APIView):
    """Registrate new user"""

    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request: Request):
        # вытаскиваем данные из запроса
        user = request.data

        # обрабатываем данные в сериализаторе
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # возвращаем успех
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(APIView):
    """Login existing new user"""

    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request: Request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        # возвращаем успех
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditUserAPIView(APIView):
    """Edit existing user email"""

    permission_classes = (IsAuthenticated,)
    serializer_class = EditUserSerializer

    def put(self, request: Request):
        # обрабатываем данные в сериализаторе
        serializer = self.serializer_class(instance=request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # возвращаем успех
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangeUserPasswordAPIView(APIView):
    """Change user password"""

    permission_classes = (IsAuthenticated,)
    serializer_class = ChangeUserPasswordSerializer

    def put(self, request: Request):
        # вытаскиваем данные о юзере из запроса
        user = request.user

        # Добавление пользователя из запроса в контекст
        self.serializer_class.context = {'user': user}

        # обрабатываем данные в сериализаторе
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # возвращаем успех
        return Response(serializer.data, status=status.HTTP_200_OK)
