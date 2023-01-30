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
        fields = '__all__'
        widgets = {
            'article': forms.TextInput(attrs={'class': 'input__article', }),
            'product_name': forms.TextInput(attrs={'class': 'input__product_name'}),
            'product_group': forms.Select(),
            'declaration': forms.FileInput(),
            'protocol': forms.FileInput(),
            'specification': forms.FileInput(),
            'quality_certificate': forms.FileInput()
        }


    def clean(self):
        cleaned_data = super().clean()
        product_group = cleaned_data['product_group']
        if not product_group:
            msg = "укажите группу товаров"
            self.add_error('phone', msg)