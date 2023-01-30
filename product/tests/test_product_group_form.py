from django.test import TestCase
from django.urls import reverse

from product.forms import ProductGroupForm
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
