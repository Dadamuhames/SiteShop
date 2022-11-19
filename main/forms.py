from django.forms import ModelForm
from django import forms
from .models import Products, Cart, Subscribes, Comments
from django.forms.widgets import NumberInput, TextInput, FileInput, Textarea,  EmailInput
import django_filters
from .models import Products

class AddproductFrom(ModelForm):
    files = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'multiple': True, 'class' : 'img-inp'}), required=False)
    class Meta:
        model = Products
        fields = ['prod_name',
                  'deskription', 'information', 'category', 'post_category']

        category = forms.ChoiceField(label='Category'),
        post_category = forms.ChoiceField(label='Post Category', choices=[])
        widgets = {
            'prod_name' : TextInput(attrs= {
                'placeholder': "Product name"
            }),
            'price': NumberInput(attrs={
                'placeholder': "Price"
            }),
            'deskription': Textarea(attrs={
                'placeholder': "Product deskription"
            }),
            'information': Textarea(attrs={
                'placeholder': "Product information"
            }),
        }


class AddToCart(ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']

        size = forms.ChoiceField(label='Size')


        widgets = {
            'quantity' : NumberInput(attrs={
                'class': 'act-inp',
                'min' : '1', 
                'value': '1',
                'id' : "nbm-inp",
            })
        }





class EmailInput(forms.ModelForm):
    class Meta:     
        model = Subscribes
        fields = ['email']

        widgets = {
            'email' : EmailInput(attrs={
                'class':"email-past search",
                
            })
        }


class Comment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text', 'product']

        widgets = {
            'text' : Textarea(attrs={
                'placeholder': "Text your view",
                'class': 'comment-input drop-inp'
            }),
            'product': forms.HiddenInput()
        }


class ProductFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()

    class Meta:
        model = Products
        fields = ['category', 'price', 'post_category']
