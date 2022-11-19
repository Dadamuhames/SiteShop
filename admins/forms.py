from dataclasses import fields
from django.forms import ModelForm
from django import forms 
from main.models import Categories, Products, Cart, Subscribes, Comments, ProductVariants, Atributs, AtributParams
from django.forms.widgets import NumberInput, TextInput, FileInput, Textarea,  EmailInput
from django.contrib.auth.models import User, Group
import django_filters


class EditProduct(forms.ModelForm):
    price = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control mb-2',
        'min': 1,
    }))
    qty = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control mb-2',
        'min': 0,
    }))

    class Meta:
        model = Products
        fields = ['prod_name', 'deskription', 'status', 'information', 'category', 'post_category']


        widgets = {
            'prod_name': forms.TextInput(attrs={
                'class': 'form-control mb-2',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select mb-2'
            }),
            'deskription': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'style': "resize: none",
                'placeholder': 'Text product\'s description...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select mb-2',
                'id': 'category-select'
            }),
            'post_category': forms.Select(attrs={
                'class': 'form-select mb-2',
                'id': 'post_ctg'
            }),
            'information': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'style': "resize: none",
                'placeholder': 'Text product\'s description...'
            }),

        }


class PostCtgField(forms.CharField):

    def to_python(self, value):
        if value in self.empty_values:
            return self.empty_value
        
        lst = str(value).replace(']', '').replace("[", '').split(',')
        new_lst = []

        for item in lst:
            tpl = tuple(item.replace('}', '').replace(
                '{', '').replace('"', "").split(":"))
            new_lst.append({tpl[0]: tpl[1]})

        return new_lst

    def prepare_value(self, value):
        if value is None:
            return None
        lst = str(value).replace(']', '').replace("[", '').split(',')
        new_lst = []

        for item in lst:
            tpl = tuple(item.replace('}', '').replace(
                '{', '').replace('"', "").split(":"))
            new_lst.append({tpl[0]: tpl[1]})

        return new_lst

    def prepare_value(self, value):
        if value is None:
            return None
        return ', '.join([val['value'] for val in value])


class AddCtg(forms.ModelForm):
    kt_ecommerce_add_category_meta_keywords = PostCtgField(
        widget=forms.TextInput(attrs={'class': 'form-control mb-2', 'id': 'kt_ecommerce_add_category_meta_keywords'}))

    class Meta:
        model = Categories
        fields = '__all__'


        widgets = {
            'category_name': forms.TextInput(attrs={
                'class': "form-control mb-2",
       			'placeholder': "Category name"
            }),
            'ctg_avatar': forms.FileInput(attrs={
                'accept':".png, .jpg, .jpeg"
            }),
            'deskription': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'style': "resize: none",
                'placeholder': 'Text category description...'
            }),
        }


class FilterUsers(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['groups']



class FilterProducts(django_filters.FilterSet):
    class Meta:
        model = Products
        fields = ['status', 'prod_name']



class ProdVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariants
        fields = ['product', 'qty', 'price', 'color']


        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select mb-2'
            }),
            'qty': forms.NumberInput(attrs={
                'class': 'form-control mb-2'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control mb-2'
            })
        }