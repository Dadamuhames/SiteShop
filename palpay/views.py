from paycomuz.views import MerchantAPIView
from django.urls import path
from paycomuz import Paycom
from functools import reduce
from http.client import HTTPResponse
from itertools import product
from msilib.schema import File
from pickletools import read_uint1
import re
from urllib import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from .models import OrderedProducts, Orders
from .forms import MakeOrder, ChangeStatus
from main.models import Cart, Products, Files, ProductVariants
from .models import Orders, OrderedProducts, OrderHistory
from account.views import get_cart_items
from django.views.generic import DetailView, ListView, UpdateView, FormView
import datetime
from django.contrib.auth.models import User






# Create youvr iews here.
def buy_page(request):
    buying = 'Plural'
    errors = ''
    if request.session.get('order_errors'):
        errors = request.session['order_errors']
        del request.session['order_errors']
    cart = get_cart_items(request)[::-1]
    if not cart:
        return redirect("home-page")
    if len(cart) > 0:
        total = 0
        if request.session.get('cart'):
            for it in cart:
                total += int(it['quant']) * it['price']
            form = MakeOrder(
                initial={'price': total, 'your_number': '+998'})
            for i in range(len(cart)):
                cart[i]['id'] = i
        return render(request, 'palpay/buy.html', {'form': form, 'cart': cart, 'total': total, 'buy_type': buying, 'errors': errors})
        
    
    else:
        return redirect(request.META.get('HTTP_REFERER'))
    


def make_order(request):
    form = MakeOrder(request.POST)
    buy_type = request.POST.get('buying_type')
    form_items = ''
    if request.session.get('cart'):
        if buy_type == 'Plural':
            cart_items = [it for it in list(request.session['cart']) if it['active'] == 'True']
        elif buy_type == 'Single':
            cart_items = [it for it in list(request.session['cart']) if it['active'] == 'False']


        prod = Products.objects.get(id=str(cart_items[0]['product']))
        variant = ProductVariants.objects.get(id=str(cart_items[0]['product_variant']))
        imgs = variant.image.first()
        if form.is_valid():
            form_items = form.save(commit=False)
            date = datetime.datetime.now()
            total = 0
            for it in cart_items:
                total += float(it['price'])
            form_items.price = total

            if request.user.is_authenticated:
                form_items.user = request.user
            else:
                if not request.session.session_key:
                    request.session.cycle_key()
                form_items.session = request.session.session_key

            form_items.order_img = imgs.file
            form_items.save()
            for it in cart_items:
                pd = Products.objects.get(id=str(it['product']))
                var = ProductVariants.objects.get(id=str(it['product_variant']))
                OrderedProducts.objects.create(
                    order=form_items,
                    img= Files.objects.filter(contact=var).first().file,
                    product=Products.objects.get(id=it['product']),
                    variant=var,
                    quantity=it['count'],
                    total=it['price']
                )

            if buy_type == 'Plural':
                for it in list(request.session.get('cart')):
                    if it['active'] == 'True':
                        request.session['cart'].remove(it)
                        request.session.modified = True
            elif buy_type == 'Single':
                for it in list(request.session.get('cart')):
                    if it['active'] == 'False':
                        request.session['cart'].remove(it)
                        request.session.modified = True


        else:
            request.session['order_errors'] = form.errors
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))

    OrderHistory.objects.create(
        order= form_items,
        status=form_items.status,
        comment=f'Order created by costumer',
        date=str(datetime.date.today())
    )
    messages.add_message(request,  messages.SUCCESS, 'Order seccsesfuly accepted')
    return redirect('my_orders')



def control_orders(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Orders.objects.order_by('-id')
        accepted = Orders.objects.filter(status='Accepted').order_by('-id')
        performed = Orders.objects.filter(status='Performed').order_by('-id')
        delivered = Orders.objects.filter(status='Delivered').order_by('-id')
        form = ChangeStatus()
        messages = get_messages(request)
        data = {
            'orders': orders, 
            'accepted': accepted,
            'performed': performed,
            'delivered': delivered,
            'form': form,
            'messages': messages
        }


        return render(request, 'palpay/orders.html', data)

    else:
        return redirect('home-page')



def change_staus(request, ord_id):
    if request.user.is_authenticated and request.user.is_superuser:
        form = ChangeStatus(request.POST)
        form.save(commit=False)
        order = Orders.objects.get(id=ord_id)
        order.status = form.cleaned_data['status']
        order.save()

        messages.add_message(request, messages.SUCCESS, '(Order №{})Order\'s status seccsesfuly updated'.format(ord_id))
        return redirect(request.META.get('HTTP_REFERER'))


def buyProduct(request):
    buying = 'Single'
    form = request.session.get('form')
    prim_key = str(form['prim_key'])
    variant = str(form['var'])
    qunt = form['qunt']
    pd = Products.objects.get(id=prim_key)
    var  = ProductVariants.objects.get(id=variant)
    img = var.image.first()
    total = var.price * qunt

    if not request.session.get('cart'):
        request.session['cart'] = list()
    else:
        request.session['cart'] = list(request.session['cart'])
        
    
    if variant in [str(it['product_variant']) for it in request.session['cart'] if it['active'] == 'False']:
        for it in request.session['cart']:
            if str(it['product_variant']) == variant and it['active'] == 'False':
                cart_it = it

    else:
        for it in request.session['cart']:
            if it['active'] == 'False':
                request.session.get('cart').remove(it)
                request.session.modified = True

        request.session['cart'].append({
            'product': pd.id,
            'name': pd.prod_name,
            'price': var.price,
            'product_variant': var.id,
            'count': qunt,
            'active': 'False',
        })

        cart_it = list(request.session['cart'])[-1]

            

    cart = [{
        'variant': var.id,
        'name': pd.prod_name,
        'price': var.price,
        'quant': cart_it['count'],
        'img': img.file.url,
        'active': cart_it['active']
    }]

    total = float(var.price) * int(cart[0]['quant'])
    
    form = MakeOrder(
        initial={'price': total, 'your_number': '+998'})
    return render(request, 'palpay/buy.html', {'form': form, 'total': total, 'cart': cart, 'buy_type': buying})



class ViewOrders(DetailView):
    model = Orders

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Orders.objects.filter(user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.cycle_key()

            return Orders.objects.filter(session=self.request.session.session_key)


    def get_context_data(self, **kwargs):
        context = super(ViewOrders, self).get_context_data(**kwargs)
        
        obj = self.get_object()
        context['form'] = ChangeStatus()
        context['is_owner'] = False
        if self.request.session.session_key:
            if obj.session == self.request.session.session_key or obj.user == self.request.user or self.request.user.is_superuser:
                context['is_owner'] = True

        final_lst = []
        context['my_order'] = False
        total_count = 0

        context['ordered_prod'] = final_lst
        context['count'] = len(final_lst)
        context['total_count'] = total_count
        
        return context

    template_name = 'palpay/order_view.html'
    context_object_name = 'order'
        
        

def my_orders(request):
    my_order = True
    orders = []
    accepted = []
    performed = []
    delivered = []
    messages = get_messages(request)
    if request.user.is_authenticated:
        orders = Orders.objects.filter(user=request.user).exclude(status='Canseled').order_by("-id")    
        accepted = Orders.objects.filter(user=request.user).filter(status='Accepted').order_by('-id')
        performed = Orders.objects.filter(user=request.user).filter(status='Performed').order_by('-id')
        delivered = Orders.objects.filter(user=request.user).filter(status='Delivered').order_by('-id')
    else:
            if not request.session.session_key:
                request.session.cycle_key()
            s_key = request.session.session_key
            orders = Orders.objects.filter(session=s_key).order_by('-id')
            accepted = Orders.objects.filter(session=s_key).filter(
                status='Accepted').order_by('-id')
            performed = Orders.objects.filter(session=s_key).filter(
                status='Performed').order_by('-id')
            delivered = Orders.objects.filter(session=s_key).filter(
                status='Delivered').order_by('-id')

    data = {
        'orders': orders,
        'accepted': accepted,
        'performed': performed,
        'delivered': delivered,
        'my_order': my_order,
        'messages': messages
    }

    return render(request, 'palpay/orders.html', data)


def cansel_order(request, id):
    order = Orders.objects.get(id=id)
    if order.status == 'Accepted':
        order.status = 'Canseled'
        order.save()

        OrderHistory.objects.create(
            order=order,
            status='Canseled',
            comment=f'Order canseled by costumer',
            date=str(datetime.date.today())
        )

    messages.add_message(request, messages.SUCCESS,
                         'Order seccsesfuly canseled')
    return redirect('my_orders')




#Payme
class CheckOrder(Paycom):
    def check_order(self, amount, account, *args, **kwargs):
        return self.ORDER_FOUND

    def successfully_payment(self, account, transaction, *args, **kwargs):
        print(account)

    def cancel_payment(self, account, transaction, *args, **kwargs):
        print(account)
      

class TestView(MerchantAPIView):
    VALIDATE_CLASS = CheckOrder