from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.serializers import UserSerializer


class UserApiTestCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(username="test1", password="test1234")
        self.user2 = User.objects.create_user(username="test2", password="test1234")
        self.user3 = User.objects.create_user(username="test3", password="test1234")

    def test_get(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        serializer_data = UserSerializer([self.user1, self.user2, self.user3], many=True).data
        self.assertEqual(serializer_data, response.data )

