from django.forms import ModelForm
from django import forms

from product.models import GroupProductModel, ProductModel


class ProductGroupForm(ModelForm):
    class Meta:
        model = GroupProductModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductGroupForm, self).__init__(*args, **kwargs)
        self.fields['group_title'].label = "название группы"
        self.fields['group_title'].widget.attrs['class'] = 'product__form_input'


class ProductForm(ModelForm):
    class Meta:
        model = ProductModel
        fields = ('article', 'product_name','price','declaration', 'protocol', 'specification', 'quality_certificate')
        widgets = {
            'article': forms.TextInput(attrs={'class': 'input__article', }),
            'product_name': forms.TextInput(attrs={'class': 'input__product_name'}),
            'declaration': forms.FileInput(),
            'protocol': forms.FileInput(),
            'specification': forms.FileInput(),
            'quality_certificate': forms.FileInput(),
            'price':forms.NumberInput()
        }
