from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from client.models import ClientModel


class ClientTestView(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            username = 'testr',
            password = 'Rem12345'
        )
        self.user_test = User.objects.create(
            username = 'user_test',
            password = 'Rem12345'
        )
        self.my_client=ClientModel.objects.create(
            owner_manager= self.user_test,
            name= 'testClien',
            phone= '8379035485215'
        )

    def test_client_add_view(self):
        url = reverse('add_client')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "client/add_client.html")

    def test_client_add_view_not_auth(self):
        url = reverse('add_client')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')


    def test_client_all_view(self):
        url = reverse('all_clients')
        expected_response = {'id': self.my_client.id, 'face_contact': None, 'name': 'testClien', 'phone': '8379035485215'}
        self.client.force_login(User.objects.get_or_create(username='user_test')[0])
        response = self.client.get(url)
        self.assertEqual(response.context['clients'][0], expected_response)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "client/all_clients.html")

    def test_client_all_view_not_auth(self):
        url = reverse('all_clients')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_client_detail_view_get(self):
        url = reverse('detail_client', kwargs={'id_client': self.my_client.id})
        self.client.force_login(User.objects.get_or_create(username='test')[0])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "client/detail_client.html")

    def test_client_detail_view_get_not_auth(self):
        url = reverse('detail_client', kwargs={'id_client': self.my_client.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_client_detail_view_post(self):
        url = reverse('detail_client', kwargs={'id_client': self.my_client.id})

        self.client.force_login(User.objects.get_or_create(username='test')[0])
        data = {
            'client': True,
            'name' : 'testClien',
            'phone' :'837903548341'
        }

        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.my_client.refresh_from_db()
        self.assertEqual(self.my_client.phone, '837903548341')
        self.assertTemplateUsed(response, 'client/detail_client.html')

    def test_client_detail_view_post_not_auth(self):
        url = reverse('detail_client', kwargs={'id_client': self.my_client.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_client_delete_view(self):
        url = reverse('delete_client', kwargs={'id_client': self.my_client.id})
        self.client.force_login(User.objects.get_or_create(username='user_test')[0])
        count_client = ClientModel.objects.filter(owner_manager= self.user_test).count()
        self.assertEqual(1, count_client)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/client/client_all/')
        count_client = ClientModel.objects.filter(owner_manager=self.user_test).count()
        self.assertEqual(0, count_client)

    def test_client_delete_view_not_auth(self):
        url = reverse('delete_client', kwargs={'id_client': self.my_client.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_client_delete_DoesNotExist(self):
        self.client.force_login(User.objects.get_or_create(username='user_test')[0])
        url = reverse('delete_client', kwargs={'id_client': '234'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/errors_client.html')







