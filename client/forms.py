from django import forms
from .models import ClientModel


class ClientForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = ['name', 'phone', 'phone2', 'phone3',
                  'face_contact', 'inn', 'fact_address',
                  'jurist_address', 'site', 'mail'
            , 'activity', 'agreement']

    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "название юр лица"
        self.fields['name'].widget.attrs['class'] = 'client__form_input'

        self.fields['phone'].label = "телефон"
        self.fields['phone'].widget.attrs['class'] = 'client__form_input'

        self.fields['phone2'].label = "телефон №2"
        self.fields['phone2'].widget.attrs['class'] = 'client__form_input'

        self.fields['phone3'].label = "телефон №3"
        self.fields['phone3'].widget.attrs['class'] = 'client__form_input'

        self.fields['mail'].label = "почта"
        self.fields['mail'].widget.attrs['class'] = 'client__form_input'

        self.fields['inn'].label = "ИНН"
        self.fields['inn'].widget.attrs['class'] = 'client__form_input'

        self.fields['fact_address'].label = "факт. адрес"
        self.fields['fact_address'].widget.attrs['class'] = 'client__form_input'
        self.fields['fact_address'].widget.attrs['rows'] = '5'

        self.fields['jurist_address'].label = "юр. адрес"
        self.fields['jurist_address'].widget.attrs['class'] = 'client__form_input'
        self.fields['jurist_address'].widget.attrs['rows'] = '5'

        self.fields['site'].label = "сайт"
        self.fields['site'].widget.attrs['class'] = 'client__form_input'

        self.fields['mail'].label = "электронная почта"
        self.fields['mail'].widget.attrs['class'] = 'client__form_input'

        self.fields['activity'].label = "примечание"
        self.fields['activity'].widget.attrs['class'] = 'client__form_input'
        self.fields['activity'].widget.attrs['rows'] = '5'

        self.fields['agreement'].label = "соглосование"
        self.fields['agreement'].widget.attrs['class'] = 'client__form_input'

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        phone2 = cleaned_data.get('phone2')
        phone3 = cleaned_data.get('phone3')
        inn = cleaned_data.get('inn')
        if phone:

            if len(phone) > 12:
                msg = "не корректный номер телефона"
                self.add_error('phone', msg)
        if phone2:
            if len(phone2) > 12:
                msg = "не корректный номер телефона"
                self.add_error('phone', msg)
        if phone3:
            if len(phone3) > 12:
                msg = "не корректный номер телефона"
                self.add_error('phone', msg)
        if inn:
            if len(inn) != 12:
                msg = "не коректный ИНН"
                self.add_error('inn', msg)
