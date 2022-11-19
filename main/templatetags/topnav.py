from django import template
from django.contrib.auth.models import User
from main.models import Cart, Files, Products, ProductVariants
from django.core.cache import cache, caches
# экземпляр класса, в котором все наши теги будут зарегистрированы
register = template.Library()
# регистрируем наш тег, который будет выводить шаблон right_sidebar.html


# В кавычках вводите путь до шаблона! он может быть у каждого свой!
@register.inclusion_tag("main/tags/topnav.html", takes_context=True)
def show_topnav(context):
    final_lst = []
    request = context['request']
    total = 0

    has_perm = request.user.has_perm("auth.view_admin")
    #if request.user.is_authenticated:
    #    final_lst = Cart.objects.filter(owner=request.user).filter(active=True)
    #    total = sum([it.price for it in final_lst])


    #else:
    if request.session.get('cart'):
        cart_items = [it for it in list(request.session.get('cart')) if it['active'] == 'True']
        for prods in cart_items:
            try:
                pd = Products.objects.get(id=str(prods['product']))
                variant = ProductVariants.objects.get(id=prods['product_variant'])
                final_lst.append({
                    'product': pd,
                    'variant': variant,
                    'price': prods['price'],
                    'image': prods['file']['url'],
                    'quantity': prods['count'],
                    'active': prods['active']
                })
                print(final_lst)
            except:
                request.session['cart'].remove(prods)

        total = sum([it['price'] for it in cart_items])


    return {'user': request.user, 'cart' : final_lst[::-1], 'len': len(final_lst), 'total': total, 'has_perm': has_perm}  # Возвращаем контекст
