from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class WorkPlaceTestView(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            username = 'test',
            password = 'Ref454567898'
        )

    def test_work_place_view(self):
        url = reverse('work_place')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("/work_place/work_place.html")

    def test_work_place_view_not_auth(self):
        url = reverse('work_place')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')