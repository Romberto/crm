from django.contrib.auth.models import User
from django.test import TestCase

from auth_user.forms import AuthForm


class UserAuthTestForm(TestCase):
    pass
    # def setUp(self) -> None:
    #     self.user_test = User.objects.create(
    #         username='test1',
    #         password="Rem123456"
    #     )

#     def test_user_auth_form(self):
#         data = {
#             'username':'test2',
#             'password':"Rem123456",
#             'password2':"Rem123456"
#         }
#         form = AuthForm(data=data)
#         print(form.errors)
#         users = User.objects.count()
#         self.assertEqual(users, 1)
# todo разобраться с тестами формы входа

