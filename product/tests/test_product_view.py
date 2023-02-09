from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from product.forms import ProductForm
from product.models import GroupProductModel, ProductModel, ProductPackagingModel
from users.models import Profile
import json


class ProductTestView(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            username="testUserPdoduct",
            password="Rem3432567"
        )

        self.group1 = GroupProductModel.objects.create(
            group_title="СОЛ-ПРО маргарин"
        )

    def test_product_view_get(self):
        url = reverse('products')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/products.html')

    def test_product_view_get_not_auth(self):
        url = reverse('products')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_product_group_add_view_get(self):
        url = reverse('add_product_group')
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product_group_add.html')

    def test_product_group_add_view_get_not_auth(self):
        url = reverse('add_product_group')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_product_group_add_view_post_not_auth(self):
        url = reverse('add_product_group')
        data = {'group_title': "СОЛ-ПРО майонез"}
        response = self.client.post(url, data=data, follow=True)
        count_product_group = GroupProductModel.objects.count()
        self.assertEqual(count_product_group, 1)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth_user/auth.html')

    def test_product_group_add_view_post(self):
        url = reverse('add_product_group')
        data = {'group_title': "СОЛ-ПРО майонез"}
        self.client.force_login(self.user)
        response = self.client.post(url, data=data, follow=True)
        count_product_group = GroupProductModel.objects.count()
        self.assertEqual(count_product_group, 2)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/products.html')

    def test_product_group_add_view_post_uniq(self):
        data = {'group_title': "СОЛ-ПРО маргарин"}
        url = reverse('add_product_group')
        self.client.force_login(self.user)
        response = self.client.post(url, data=data, follow=True)
        self.assertFormError(response, 'form', 'group_title', 'Группа продукта с таким Group title уже существует.')


class TestAjaxProduct(TestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(
            username='usertest3',
            password='Redf324564'
        )
        self.admin = User.objects.create(
            username='admintest',
            password='Redf324564'
        )
        self.profile = Profile.objects.create(
            user=self.admin,
            position='DR',
            phone='89020340506'
        )

        self.profile1 = Profile.objects.create(
            user=self.user1,
            position='MP',
            phone='89020340506'
        )

        self.group = GroupProductModel.objects.create(
            group_title='жир'
        )

    def test_product_ajax(self):
        expend_data = {'error': True, 'msg': 'группы не существует'}
        url = reverse('edit_product_group')
        url = url + '?id=7&val=маргарин'
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), expend_data)

    def test_product_ajax_no_auth(self):
        expend_data = {'error': True, 'msg': 'не зарегистрированный пользователь'}
        url = reverse('edit_product_group')
        url = url + '?id=7&val=маргарин'
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), expend_data)

    def test_product_ajax_edit_second(self):
        expend_data = {'error': True, 'msg': 'группа с таким названием уже есть'}
        url = reverse('edit_product_group')
        url = url + '?id=' + str(self.group.id) + '&val=жир'
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), expend_data)

    def test_product_ajax_edit_null(self):
        expend_data = {'error': True, 'msg': 'пустые значения не допустимы'}
        url = reverse('edit_product_group')
        url = url + '?id=1&val='
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), expend_data)

    def test_product_ajax_edit_no_director(self):
        expend_data = {'error': True, 'msg': 'менять название может только директор'}
        url = reverse('edit_product_group')
        url = url + '?id=' + str(self.group.id) + '&val=vgf'
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), expend_data)

    def test_product_ajax_edit_ok(self):
        expend_data = {'error': False}
        url = reverse('edit_product_group')
        url = url + '?id=' + str(self.group.id) + '&val=змж'
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), expend_data)
        self.assertEqual(str(GroupProductModel.objects.get(id=self.group.id)), 'змж')


class TestAjaxProductDelete(TestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create(
            username='usertest3',
            password='Redf324564'
        )
        self.admin = User.objects.create(
            username='admintest',
            password='Redf324564'
        )
        self.profile = Profile.objects.create(
            user=self.admin,
            position='DR',
            phone='89020340506'
        )
        self.profile1 = Profile.objects.create(
            user=self.user1,
            position='MP',
            phone='89020340506'
        )
        self.group = GroupProductModel.objects.create(
            group_title='жир'
        )

    def test_ajax_product_delete_no_auth(self):
        expend_data = {'error': True, 'msg': 'не зарегистрированный пользователь'}
        url = reverse('delete_product_group')
        url = url + '?id=1'
        self.client.force_login(self.user1)
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), expend_data)

    def test_ajax_product_delete_no_product(self):
        expend_data = {'error': True, 'msg': 'группа отсутсевует'}
        url = reverse('delete_product_group')
        url = url + '?id=6'
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), expend_data)

    def test_ajax_product_delete_ok(self):
        expend_data = {'error': False}
        url = reverse('delete_product_group')
        url = url + '?id=' + str(self.group.id)
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), expend_data)
        self.assertEqual(GroupProductModel.objects.count(), 0)

class TestProductItem(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            username = 'testuser',
            password = 'TestPass'
        )
        self.admin = User.objects.create(
            username='testAdmin',
            password='TestPass'
        )

        self.groupe = GroupProductModel.objects.create(
            group_title = 'ZMJ'
        )

        self.product = ProductModel.objects.create(
            article = '33100',
            product_name = 'провансаль',
            product_group = self.groupe
        )

    def test_product_list_view_ok(self):
        url = reverse('product_list', kwargs={'id': self.groupe.id})
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product_list.html')

    def test_product_list_view_no_auth(self):
        url = reverse('product_list', kwargs={'id': self.groupe.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_add_product_view(self):
        url = reverse('add_product', kwargs={'id': self.groupe.id})
        self.client.force_login(self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product_add.html')

    def test_add_product_view_no_auth(self):
        url = reverse('add_product', kwargs={'id': self.groupe.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_add_product_view_post(self):
        data = {
            'article': '33500',
            'product_name': 'провансаль',
            'product_group': self.groupe.id,
            'product_type': 'T'
        }
        self.client.force_login(self.user)
        url = reverse('add_product', kwargs={'id': self.groupe.id})
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        count_product = ProductModel.objects.count()
        self.assertEqual(count_product, 2)

    def test_edit_product_view_get(self):
        url = reverse('edit_product', kwargs={'id': self.product.id})
        self.client.force_login(self.admin)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product/product_edit.html')


    def test_edit_product_view_get_no_auth(self):
        url = reverse('edit_product', kwargs={'id': self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_edit_product_view_product_post(self):
        url = reverse('edit_product', kwargs={'id': self.product.id})
        self.client.force_login(self.admin)
        data = {'article': '33500',
                'product_type':'T',
                'product_name': 'провансаль',
                'product_group': self.groupe.id,
                'product':True
                }
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/product/'+str(data['product_group']))
        self.assertTemplateUsed(response, 'product/product_list.html')
        product = ProductModel.objects.get(id=self.product.id)
        self.assertEqual(product.article, '33500')

    def test_edit_product_view_packing_post(self):
        url = reverse('edit_product', kwargs={'id': self.product.id})
        self.client.force_login(self.admin)
        data = {'packing_name': 'тарра',
                'quantity_element_in': 3,
                'netto': 13.6,
                'brutto': 14.2,
                'quantity_box': 40,
                'packing':True
                }
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductPackagingModel.objects.count(), 1)
        obj= ProductPackagingModel.objects.get(id=1)
        self.assertEqual(obj.pallet_weight_netto, 544)
        self.assertEqual(obj.pallet_weight_brutto, 568)
        self.assertTemplateUsed(response, 'product/product_list.html')
        self.assertRedirects(response, '/product/' + str(self.product.product_group.id))

    def test_edit_product_view_packing_post_error(self):
        expend_data = {'brutto': ['масса брутто должна быть больше массы нетто']}
        url = reverse('edit_product', kwargs={'id': self.product.id})
        self.client.force_login(self.admin)
        data = {'packing_name': 'тарра',
                'netto': 13.6,
                'brutto': 13,
                'quantity_box': 40,
                'packing': True
                }
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.context['form_packing'].errors, expend_data)

    def test_edit_product_view_packing_post_error_equal(self):
        expend_data = {'brutto': ['масса брутто должна быть больше массы нетто']}
        url = reverse('edit_product', kwargs={'id': self.product.id})
        self.client.force_login(self.admin)
        data = {'packing_name': 'тарра',
                'netto': 13,
                'brutto': 13,
                'quantity_box': 40,
                'packing': True
                }
        response = self.client.post(url, data=data, follow=True)
        self.assertEqual(response.context['form_packing'].errors, expend_data)


    def test_delete_product_view_ajax(self):
        expend_data = {'error': False}
        url = reverse('delete_product')
        url = url + '?id=' + str(self.product.id)
        self.client.force_login(self.admin)
        response = self.client.get(url)

        self.assertEqual(ProductModel.objects.count(), 0)
        self.assertEqual(json.loads(response.content), expend_data)

