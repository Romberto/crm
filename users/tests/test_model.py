from django.contrib.auth.models import User
from django.test.testcases import TestCase

from users.models import Profile


class TestModelCRM(TestCase):

    def setUp(self) -> None:
        self.user=User.objects.create_user(
            username='test',
            password='qwer1234Q'
        )
        self.profile=Profile.objects.create(
            user=self.user,
            position='MP',
            phone='+79031235423'
        )

    def test_model(self):
        user = User.objects.count()
        self.assertEqual(1, user)
        pos = self.user.profile.position
        self.assertEqual("MP", pos)

    def test_model_profile(self):
        profile_count = Profile.objects.count()
        self.assertEqual(profile_count, 1)
        phone = self.profile.phone
        self.assertEqual(phone, '+79031235423')
        position = self.profile.position
        self.assertEqual(position, "MP")
        user = self.profile.user
        self.assertEqual(user, self.user)