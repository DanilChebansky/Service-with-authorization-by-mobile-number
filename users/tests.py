from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from users.services import create_invite_code


class UserTest(APITestCase):
    """Тестирование регистрации пользователя"""

    def setUp(self):
        self.user = User.objects.create(
            phone="79000000000",
            invite_code="12Hk1p",
            email="dan@ya.ru",
            city="Kurchatov",
            is_superuser=True,
            is_staff=True,
        )
        self.user1 = User.objects.create(
            phone="79000000001", invite_code="LeO151", invite_input="12Hk1p"
        )

    def test_user_create(self):
        url = reverse("users:login")
        data = {
            "phone": "79000000002",
            "invite_code": "Le3456",
            "city": "Kursk",
            "email": "dan3@ya.ru",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 3)

    def test_user_update(self):
        """Проверяем обновление полей пользователя"""
        self.user.email = "dan1@ya.ru"
        self.user.invite_input = "12Hk1p"
        self.user.city = "Kursk"
        self.user.save()
        self.assertEqual(self.user.email, "dan1@ya.ru")
        self.assertEqual(self.user.invite_input, "12Hk1p")
        self.assertEqual(self.user.city, "Kursk")

    def test_create_invite_code(self):
        """Тестирование генерации кода авторизации"""
        code = create_invite_code()
        self.assertTrue(len(code) == 6)
        self.assertFalse(code.isdigit())

    def test_user_delete(self):
        """Тестирование удаления пользователя"""
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user_delete", args=(self.user1.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 1)

    def test_user_list(self):
        """Тестирование списка пользователей"""
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user_list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.user.pk,
                "phone": self.user.phone,
                "email": self.user.email,
                "city": self.user.city,
                "invite_code": self.user.invite_code,
                "invite_input": self.user.invite_input,
                "invitation_list": [self.user1.phone],
            },
            {
                "id": self.user1.pk,
                "phone": self.user1.phone,
                "email": self.user1.email,
                "city": self.user1.city,
                "invite_code": self.user1.invite_code,
                "invite_input": self.user1.invite_input,
                "invitation_list": [],
            },
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
