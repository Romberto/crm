from django import forms

from client.models import ClientModel
from product.models import ProductModel
from trade.models import TradeModel, TradeItemModel, TradeAgentItem


class TradeForm(forms.ModelForm):
    class Meta:
        model = TradeModel
        fields = ('client', 'specification')


    def __init__(self, *args, **kwargs):
        super(TradeForm, self).__init__( *args, **kwargs)
        self.fields['client'].queryset = ClientModel.objects.filter(role='P')




class TradeItemForm(forms.ModelForm):
    class Meta:
        model = TradeItemModel
        fields = ('product', 'count')


    def __init__(self, *args, **kwargs):
        super(TradeItemForm, self).__init__(*args, **kwargs)
        self.fields['product'].label = "продукт"
        self.fields['product'].widget.attrs['class'] = 'trade__input'

        self.fields['count'].label = "количество"
        self.fields['count'].widget.attrs['class'] = 'trade__input'

    # def clean(self):
    #     cleaned_data = super().clean()

class TradeAgentForm(forms.ModelForm):

    class Meta:
        model = TradeAgentItem
        fields = ('id','product', 'count', 'date_delivery', 'price')

    def __init__(self, *args, **kwargs):

        super(TradeAgentForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['type'] = 'hidden'




