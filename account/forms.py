from dataclasses import fields
from tkinter import Widget
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django.forms.widgets import FileInput
from django.contrib.auth.forms import UserCreationForm
import re


class RegistrForm(UserCreationForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.CharField(max_length=256)

    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_password(self):
        cd = self.cleaned_data
        print(cd)
        if cd['password1'] != cd['password2']:
            raise forms.ValidationError(('Passwords don\'t match.'), code='Invalid')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if cd['email'] in [it.email for it in User.objects.all()]:
            raise forms.ValidationError(
                ('User with this email is already registered'))
        return cd['email']


class LoginForm(forms.Form):
    username = forms.CharField(help_text='Логин')
    password = forms.CharField(widget=forms.PasswordInput, help_text='Пароль')


class ChangeBio(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']

        widgets = {
            'bio' : forms.Textarea(attrs={
                "class" : "abt-txt",
                "placeholder": "Text something about you..."
            })
        }


class ChangeAcount(forms.ModelForm):
    def names_valid(val):
        username = str(val)

        if username.isnumeric():
            raise forms.ValidationError(
                ("Field is invalid")
            )

        return username



    username = forms.CharField(max_length=255, validators=[names_valid])
    first_name = forms.CharField(max_length=255, validators=[names_valid])
    last_name = forms.CharField(max_length=255, validators=[names_valid])
    class Meta:
        model = Profile
        fields = ['instagram', 'facebook', 'wk', 'twitter', 'tel']


    def clean_first_name(self):
        name = str(self.cleaned_data['first_name'])

        if name.isnumeric():
            raise forms.ValidationError(
                ("First name is invalid")
            )

        return name

    def clean_last_name(self):
        name = str(self.cleaned_data['last_name'])

        if name.isnumeric():
            raise forms.ValidationError(
                ("Last name is invalid")
            )

        return name

    def clean_tel(self):
        nbm = self.cleaned_data['tel']
        number_temp = r"\+998\d{9}"
        if nbm is not None:
            if bool(re.match(number_temp, nbm)) == False:
                raise forms.ValidationError(
                    ("Your telephone number is invalid")
                )
        return nbm

    def clean_instagram(self):
        lnk = self.cleaned_data['instagram']
        if lnk is not None:
            if bool(re.match('https://instagram.com/', lnk)) == False:
                raise forms.ValidationError(
                    ('Your instagram link is invalid')
                )

        return lnk

    def clean_wk(self):
        lnk = self.cleaned_data['wk']
        if lnk is not None:
            if bool(re.match('https://vk.ru/', lnk)) == False:
                raise forms.ValidationError(
                    ('Your vk link is invalid')
                )

        return lnk

    def clean_facebook(self):
        lnk = self.cleaned_data['facebook']
        if lnk is not None:
            if bool(re.match('https://facebook.com/', lnk)) == False:
                raise forms.ValidationError(
                    ('Your facebook link is invalid')
                )

        return lnk

    def clean_twitter(self):
        lnk = self.cleaned_data['twitter']
        if lnk is not None:
            if bool(re.match('https://twitter.com/', lnk)) == False:
                raise forms.ValidationError(
                    ('Your twitter link is invalid')
                )

        return lnk

