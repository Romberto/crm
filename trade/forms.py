from django import forms

from trade.models import TradeModel, TradeItemModel


class TradeForm(forms.ModelForm):
    class Meta:
        model = TradeModel
        fields = ('stage_name', 'client', 'specification')

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
