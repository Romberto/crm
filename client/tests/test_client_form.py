from pprint import pprint

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from client.forms import ClientForm
from client.models import ClientModel


class ClientTestForm(TestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(username='test1', password="Test9812")


    def test_add_form_valid(self):
        url = reverse('add_client')
        data = {'owner_manager':self.user1.id,
                'name':'name',
                'phone':'+79080230505',
                'phone2':'+79080230505',
                'phone3':'+79080230505',
                'mail':'test@mail.ru',
                'inn':'123456789123',
                'fact_address ': 'fact_address',
                'jurist_address ': 'jurist_address',
                'activity':'blalbalva',
                'face_contact':'face_contact',
                'site':'https://site.ru',
                'agreement':True,}


        self.client.force_login(User.objects.get_or_create(username='test1')[0])
        form = ClientForm(data)
        self.assertTrue(form.is_valid())
        response = self.client.post(url, data=data, follow=True)
        self.assertTrue(form.is_valid())
        client_count = ClientModel.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/all_clients.html')
        self.assertEqual(1, client_count)


    def test_add_form_no_valid_phone(self):

        data = {'owner_manager': self.user1.id, 'name':'testClien', 'phone': '8379035485215'}
        form = ClientForm(data)
        self.assertFalse(form.is_valid())
        url = reverse('add_client')
        self.client.force_login(User.objects.get_or_create(username='test1')[0])
        response = self.client.post(url, data=data, follow=True)
        self.assertFormError(response ,'form','phone','не корректный номер телефона')
        self.assertEqual(response.status_code,200)

    def test_add_form_no_valid_inn(self):
        data = {'owner_manager': self.user1.id, 'name': 'testClien', 'phone': '+72392562128', 'inn':'123'}
        form = ClientForm(data)
        self.assertFalse(form.is_valid())
        url = reverse('add_client')
        self.client.force_login(User.objects.get_or_create(username='test1')[0])
        response = self.client.post(url, data=data, follow=True)
        self.assertFormError(response ,'form','inn','не коректный ИНН')
        self.assertEqual(response.status_code,200)