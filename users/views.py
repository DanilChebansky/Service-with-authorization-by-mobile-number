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

from rest_framework.views import APIView


class UserRegisterAPIView(generics.CreateAPIView):
    """Авторизует пользователя. Если его нет в базе данных, добавляет его туда"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        return_data = {}
        if not request.data.get('phone'):
            return_data["message"] = 'Вы не ввели номер телефона'
            return Response(return_data, status=status.HTTP_400_BAD_REQUEST)
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
        password = random.randint(10000, 99999)
        user.set_password(str(password))
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
        return_data = {}
        user = User.objects.get(phone=request.data.get("phone"))
        sms = request.data.get("sms")
        if user.sms == sms:
            login(self.request, user)
            return_data['invite_code'] = user.invite_code
            return_data['message'] = "Вы успешно авторизованы"
            user.sms = ''
            user.save()
        else:
            return_data['message'] = "Код введен неправильно"
        return Response(return_data, status=status.HTTP_200_OK)


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsSelfUser]

    # def patch(self, request, *args, **kwargs):
    #     user = self.get_object()  # Получаем пользователя
    #     serializer = self.get_serializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
