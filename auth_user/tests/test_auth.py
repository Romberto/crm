from django.test import TestCase

class AuthTestCase(TestCase):
    def test_auth_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "auth_user/auth.html")






