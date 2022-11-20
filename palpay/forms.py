from asyncore import read
from dataclasses import field
from .models import OrderedProducts, Orders
from django import forms
from django.forms.widgets import TextInput, NumberInput, Select, RadioSelect, CheckboxInput
import re


class MakeOrder(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['name', 'price', 'city', 'adres', 'your_number', 'cash', 'payme', 'email', 'ship_type']

        widgets = {
            'your_number': TextInput(attrs={
                'placeholder' : 'Input your phone number',
                'id': 'nbm-input',
                'class': 'ph-nbm field'
            }),
            'name': TextInput(attrs={
                'placeholder' : 'Input your name',
                'class' : 'field'
            }),
            'price': NumberInput(attrs={
                'readonly': 'True',
                'class': 'field'
            }),
            'adres': TextInput(attrs={
                'placeholder': 'Input your adress(Area, Street, House)',
                'class': 'field'
            }),
            'city': Select(attrs={
                'class': 'filed'
            }),
           'cash': CheckboxInput(attrs={
                'class': 'choose-payment'
            }),
            'payme': CheckboxInput(attrs={
                'class': 'choose-payment'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'filed',
                'placeholder': 'Input your email adres'
            })
        }

    def clean_your_number(self):
        nbm = self.cleaned_data['your_number']
        number_temp = r"\+998\d{9}"
        print(bool(re.match(number_temp, nbm)))
        if bool(re.match(number_temp, nbm)) == False:
            raise forms.ValidationError(
                ("Your telephone number is invalid")
            )
        return nbm
        

class ChangeStatus(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['status']

        status = forms.ChoiceField()
    


        
