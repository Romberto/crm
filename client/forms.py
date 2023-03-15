import re

from django import forms
from .models import ClientModel


class ClientForm(forms.ModelForm):
    class Meta:
        model = ClientModel
        fields = ['role','name', 'phone', 'phone2', 'phone3',
                  'face_contact', 'inn', 'fact_address',
                  'jurist_address', 'site', 'mail'
            , 'activity', 'agreement', 'trend_raf', 'trend_no_raf', 'trend_manez', 'trend_licetin']


    def __init__(self, *args, **kwargs):
        super(ClientForm, self).__init__(*args, **kwargs)
        self.fields['role'].label = "покупатель/продавец"
        self.fields['role'].widget.attrs['class'] = 'client__form_input'

        self.fields['name'].label = "название юр лица"
        self.fields['name'].widget.attrs['class'] = 'client__form_input'

        self.fields['phone'].label = "телефон"
        self.fields['phone'].widget.attrs['class'] = 'client__form_input'
        self.fields['phone'].widget.attrs['placeholder'] = '+79994443322'

        self.fields['phone2'].label = "телефон №2"
        self.fields['phone2'].widget.attrs['class'] = 'client__form_input'
        self.fields['phone2'].widget.attrs['placeholder'] = '+79994443322'

        self.fields['phone3'].label = "телефон №3"
        self.fields['phone3'].widget.attrs['class'] = 'client__form_input'
        self.fields['phone3'].widget.attrs['placeholder'] = '+79994443322'

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

        self.fields['trend_raf'].label = "масло рафинорованное"
        self.fields['trend_raf'].widget.attrs['class'] = 'form_trand'

        self.fields['trend_no_raf'].label = "масло не рафинорованное"
        self.fields['trend_no_raf'].widget.attrs['class'] = 'form_trand'

        self.fields['trend_manez'].label = "майонез"
        self.fields['trend_manez'].widget.attrs['class'] = 'form_trand'

        self.fields['trend_licetin'].label = "лицетин"
        self.fields['trend_licetin'].widget.attrs['class'] = 'form_trand'


    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        phone2 = cleaned_data.get('phone2')
        phone3 = cleaned_data.get('phone3')
        inn = cleaned_data.get('inn')
        pattern = re.compile('^\+7\D*\d{3}\D*\d{3}\D*\d{2}\D*\d{2}')
        if phone:
            if not pattern.search(phone):
                msg = "запишите номер телефона через +7"
                self.add_error('phone', msg)
            elif len(phone) > 12:

                msg = "слишком длинный номер телефона"
                self.add_error('phone', msg)


        if phone2:
            if not pattern.search(phone2):
                msg = "запишите номер телефона через +7"
                self.add_error('phone2', msg)
            elif len(phone2) > 12:
                msg = "слишком длинный номер телефона"
                self.add_error('phone2', msg)
        if phone3:
            if not pattern.search(phone3):
                msg = "запишите номер телефона через +7"
                self.add_error('phone3', msg)
            elif len(phone3) > 12:
                msg = "слишком длинный номер телефона"
                self.add_error('phone3', msg)
        if inn:
            if len(inn) != 12:
                msg = "не коректный ИНН"
                self.add_error('inn', msg)
