import random
import time

from django.contrib.auth import authenticate, login

from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.validators import UniqueValidator

from users.permissions import IsSelfUser
from users.serializers import UserSerializer, ProfileSerializer, UserConfirmSerializer, UserUpdateSerializer
from users.models import User
from users.services import create_invite_code

from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


class UserRegisterAPIView(generics.CreateAPIView):
    """Авторизует пользователя. Если его нет в базе данных, добавляет его туда"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.fields['phone'].validators = [
            v for v in serializer.fields['phone'].validators
            if not isinstance(v, UniqueValidator)
        ]
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(
            phone=serializer.validated_data['phone'],
            defaults={
                'invite_code': create_invite_code()
            }
        )
        sms = random.randint(1000, 9999)
        user.sms = str(sms)
        user.save()

        time.sleep(3)
        print(sms)

        return Response(data=UserSerializer(user).data, status=status.HTTP_201_CREATED)


class UserConfirmAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserConfirmSerializer(data=request.data)
        serializer.fields['phone'].validators = [
            v for v in serializer.fields['phone'].validators
            if not isinstance(v, UniqueValidator)
        ]
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(User, phone=serializer.validated_data['phone'])
        if user.sms != serializer.validated_data['sms']:
            raise ValidationError({'sms': 'Неправильный смс-код'})

        login(self.request, user)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsSelfUser]


class UserProfileAPIView(generics.RetrieveAPIView):
    """Возвращает информацию о пользователе"""

    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsSelfUser | IsAdminUser]


class UserListAPIView(generics.ListAPIView):
    """Возвращает список пользователей"""

    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]


class UserDestroyAPIView(generics.DestroyAPIView):
    """Удаляет пользователя"""

    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]
