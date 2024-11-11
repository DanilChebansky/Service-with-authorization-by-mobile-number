import random
import time

from django.contrib.auth import authenticate, login

from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics

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
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.save(is_active=True)
            user.invite_code = create_invite_code()
        except Exception:
            user = User.objects.get(phone=request.data.get("phone"))
        finally:
            return_data["message"] = "Введите отправленный Вам на указанный телефон смс-код на странице подтверждения"
            password = random.randint(10000, 99999)
            user.set_password(str(password))
            sms = random.randint(1000, 9999)
            user.sms = str(sms)
            user.save()
            time.sleep(3)
            print(sms)

        return Response(return_data, status=status.HTTP_201_CREATED)


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


class UserUpdateAPIView(APIView):
    """Редактирует информацию о пользователе"""

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated, IsSelfUser | IsAdminUser]

    def patch(self, request):
        user = self.request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get_permissions(self):
    #     self.permission_classes = [IsAuthenticated, IsSelfUser | IsAdminUser]
    #     return [permission() for permission in self.permission_classes]


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
