from django.contrib.auth.models import User

from users.models import Profile
from users.serializers import UserSerializer
from django.test import TestCase


class UserTestSerializer(TestCase):
    def setUp(self) -> None:
        self.user6 = User.objects.create(username="test6", password="test1234")
        self.user7 = User.objects.create(username="test7", password="test1234")

        self.profile1 = Profile.objects.create(
            user=self.user6,
            position='MP',
            phone='+79031235423'
        )
        self.profile2 = Profile.objects.create(
            user=self.user7,
            position='MP',
            phone='+79031235423'
        )


    def test_user_serializer(self):
        data = UserSerializer([self.user6, self.user7], many=True).data
        expected_data = [
            {'username': 'test6',

             },

            {'username': 'test7',
            }
        ]
        self.assertEqual(expected_data, data)
