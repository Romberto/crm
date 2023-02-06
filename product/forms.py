from django.forms import ModelForm
from django import forms

from product.models import GroupProductModel, ProductModel, ProductPackagingModel


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
        fields = ('article', 'product_type','product_name','price','declaration', 'protocol', 'specification', 'quality_certificate')
        widgets = {
            'article': forms.TextInput(attrs={'class': 'input__article', }),
            'product_name': forms.TextInput(attrs={'class': 'input__product_name'}),
            'declaration': forms.FileInput(),
            'protocol': forms.FileInput(),
            'specification': forms.FileInput(),
            'quality_certificate': forms.FileInput(),
            'price':forms.NumberInput()

        }
    def clean(self):
        cleaned_data = super().clean()
        product_type = cleaned_data.get("product_type")

        if product_type == 'N':
            msg = "укажите тип тары продукта"
            self.add_error('product_type', msg)

class ProductPackingForm(forms.ModelForm):
    class Meta:
        model = ProductPackagingModel
        fields = ('packing_name', 'netto', 'brutto', 'quantity_box',)
        widgets = {
            'packing_name': forms.TextInput(),
            'netto': forms.NumberInput(attrs={'placeholder':'20'}),
            'brutto':forms.NumberInput(attrs={'placeholder':'20.4'}),
            'quantity_box': forms.NumberInput(attrs={'placeholder':'48'})
        }

    def clean(self):
        cleaned_data = super().clean()
        netto = cleaned_data.get("netto")
        brutto = cleaned_data.get("brutto")
        if netto >= brutto:
            msg = "масса брутто должна быть больше массы нетто"
            self.add_error('brutto', msg)

