from django import template
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from main.forms import EmailInput
from main.models import Products, Files
# экземпляр класса, в котором все наши теги будут зарегистрированы
register = template.Library()
# регистрируем наш тег, который будет выводить шаблон right_sidebar.html


# В кавычках вводите путь до шаблона! он может быть у каждого свой!
@register.inclusion_tag("main/tags/footer.html", takes_context=True)
def show_footer(context):
    request = context['request']
    products = Products.objects.order_by('-id')
    img = Files.objects.all()
    form = EmailInput()
    
    return {'form': form}
    
