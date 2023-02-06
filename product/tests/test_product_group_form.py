from django.test import TestCase
from django.urls import reverse

from product.forms import ProductGroupForm, ProductForm, ProductPackingForm
from product.models import GroupProductModel


class ProductGroupFormTestView(TestCase):

    def setUp(self) -> None:
        self.group1 = GroupProductModel.objects.create(
            group_title = "СОЛ-ПРО змж"
        )

    def test_product_group_form(self):
        data = {
            'group_title': "СОЛ-ПРО майонез"
        }
        form = ProductGroupForm(data=data)
        self.assertTrue(form.is_valid())

    def test_product_group_form_uniq(self):
        data = {
            'group_title': "СОЛ-ПРО змж"
        }
        form = ProductGroupForm(data=data)
        self.assertFalse(form.is_valid())

class TestProductItemForm(TestCase):

    def setUp(self) -> None:
        self.groupe = GroupProductModel.objects.create(
            group_title = 'майонезы'
        )


    def test_product_item_form_ok(self):
        data = {
            'article' : '33100',
            'product_name' : 'провансаль',
            'product_group' : self.groupe.id,
            'product_type': 'T'
        }
        form = ProductForm(data=data)
        self.assertTrue(form.is_valid())

    def test_product_item_form_no_art(self):
        data = {
            'product_name' : 'провансаль',
            'product_group' : self.groupe.id
        }
        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())

    def test_product_item_form_no_name(self):
        data = {
            'article' : '33100',
            'product_group' : self.groupe.id
        }
        form = ProductForm(data=data)
        self.assertFalse(form.is_valid())

class TestProductPackingForm(TestCase):

    def setUp(self) -> None:
        pass

    def test_form_packing_product_is_valid(self):
        data = {'packing_name': 'тарра',
                'netto': 13.6,
                'brutto': 14.2,
                'quantity_box': 40,
                'packing':True
                }
        form = ProductPackingForm(data=data)
        self.assertTrue(form.is_valid())

    def test_form_packing_product_is_not_valid(self):
        data = {'packing_name': 'тарра',
                'netto': 13.6,
                'brutto': 13,
                'quantity_box': 40,
                'packing':True
                }
        form = ProductPackingForm(data=data)
        self.assertFalse(form.is_valid())

