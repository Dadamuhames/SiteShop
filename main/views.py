from cProfile import Profile
from http.client import HTTPResponse
from urllib import request
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView, UpdateView, FormView
from django.views.generic.edit import ModelFormMixin
from django.db.models import Q
from main.models import Products, Files, Cart, Categories, PostCategories, Comments, Subscribes, AtributParams, Colors, ProductVariants
from .forms import AddproductFrom, AddToCart, EmailInput, Comment, ProductFilter
from account.models import Profile
from django.core.mail import send_mail
import datetime
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.cache import cache, caches
from admins.models import FAQ
from easy_thumbnails.files import get_thumbnailer

# Create your views here.
def home(request):
    products = Products.objects.filter(status='Published').order_by('-id')
    return render(request, 'main/homepage.html', {'products': products[:8]})


def add_to_cart(request):

    if not request.session.get('cart'):
        request.session['cart'] = list()


    for it in request.session['cart']:
        if it['active'] == 'False':
            request.session.get('cart').remove(it)
            request.session.modified = True

    form = AddToCart(request.POST)
    if '_cart' in request.POST:
        if form.is_valid():
            prim_key = request.POST['product']
            qunt = form.cleaned_data['quantity']
            owner = request.user
            prod = Products.objects.filter(status='Published').get(id=prim_key)
            prod_var = request.POST.get('variant')
            var = ProductVariants.objects.get(id=prod_var)

            if not request.session.get('cart'):
                request.session['cart'] = list()
            else:
                request.session['cart'] = list(request.session['cart'])

            add_data = {
                'product': prim_key, 
                'product_variant': prod_var,
                'price': var.price * qunt,
                'count': qunt,
                'active': 'True',
                'file': {'url' : get_thumbnailer(Files.objects.filter(contact=var).first().file)['cart'].url}
            }

            if not str(prod_var) in [str(it['product_variant']) for it in list(request.session.get('cart'))]:
                request.session['cart'].append(add_data)
                request.session.modified = True
                messages.add_message(request,  messages.SUCCESS, 'Seccsesfuly added to your cart')
            else:
                lst_cart = list(request.session.get('cart'))
                for i in range(len(lst_cart)):
                    if prod_var == lst_cart[i]['product_variant']:
                        request.session.get('cart').remove(lst_cart[i])
                        request.session['cart'].append(add_data)
                        messages.add_message(request,  messages.SUCCESS, 'Cart updated')

    elif '_buy' in request.POST:
        if form.is_valid():
            request.session['form'] = {
                'prim_key': request.POST.get('product'),
                'var': request.POST.get('variant'),
                'qunt': form.cleaned_data['quantity']
            }
            return redirect('buy_single_prod')

    url = request.POST.get('url')
    return redirect(url)




class ProductsView(ModelFormMixin, DetailView):
    model = Products
    success_url = '#'
    form_class = AddToCart

    def get_queryset(self):
        return Products.objects.filter(status='Published') 

    def get_context_data(self, **kwargs):
        context = super(ProductsView, self).get_context_data(**kwargs)
        
        
        context['comment_input'] = Comment(initial={'product' : context['product']})
        context['comments'] = Comments.objects.filter(product=context['product']).filter(active=True).filter(parent=None).order_by('-id')
        context['answers'] = Comments.objects.filter(product=context['product']).filter(active=True).exclude(parent=None)
        obj = self.get_object()

        if not self.request.session.get('liked'):
            self.request.session['liked'] = list()
        wishlist = list(self.request.session['liked'])

        try:
            context['liked'] = obj.id in [
                wish['id'] for wish in wishlist]
        except:
            pass

        if not self.request.session.get('cart'):
            self.request.session['cart'] = list()
        cart = list(self.request.session.get('cart'))
        context['in_cart'] = str(obj.get_default().id) in [str(it['product_variant']) for it in cart if it['active'] == 'True']
        if context['in_cart']:
            context['total'] = [it for it in cart if str(it['product_variant']) == str(obj.get_default().id) and it['active'] == 'True'][0]['price']
        else:
            context['total'] = obj.get_default().price
    
        return context

    template_name = 'main/prodpage.html'
    context_object_name = 'product'
    form_object_name = 'form_class'




    
        


@login_required
def addComents(request):
    form = Comment(request.POST)
    if form.is_valid():
        text = request.POST.get('text')
        parent_id = request.POST.get('parent')
        parent = None
        if parent_id != '':
            parent = Comments.objects.get(id=parent_id)
        prod = form.cleaned_data['product']
        act = request.user.is_superuser
        Comments.objects.create(
            user=request.user,
            product = prod,
            parent=parent,
            text = text,
            active = act,
            likes = '0',
            date = str(datetime.datetime.now())
        )

        if not act:
            messages.add_message(request, messages.INFO, 'Your comment will be added after admin\'s acception')
    

    return redirect(request.META.get('HTTP_REFERER'))



def removeFromCart(request, c_id):
    if request.session.get('cart'):
        for it in request.session['cart']:
            if str(c_id) == str(it['product_variant']):
                request.session['cart'].remove(it)
                request.session.modified = True
    messages.add_message(request,  messages.SUCCESS, 'Seccsesfuly deleted from your cart')


    
    pre_url = request.META.get('HTTP_REFERER')
    return redirect(pre_url)


class CotalogView(ListView):
    paginate_by = 8
    model = Products
    template_name = 'main/cotalog.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super(CotalogView, self).get_context_data(**kwargs)
        img_files = Files.objects.all()
        context['new'] = Products.objects.filter(
            status='Published').order_by("-id")[:8]
        context['categories'] = list(Categories.objects.all(),)
        context['post_categ'] = list(PostCategories.objects.all())

        url = self.request.get_full_path()
        if '?' in url:
            url = url.split('?')[0]
        print(url)
        context['url'] = url + '?'

        return context


    def get_queryset(self):
        return Products.objects.filter(status='Published').order_by("-id")[8:]



def about_us(request):
    return render(request, 'main/about.html')


def contact_page(request):
    return render(request, 'main/faq-pages/contacts.html')



def addproduct(request):
    if request.user.has_perm('catalog.can_add_products'):
        if request.method == 'POST':
            form = AddproductFrom(request.POST, request.FILES)
            form.post_category = request.POST.get('post_category')
            files = request.FILES.getlist('files')
            if form.is_valid():
                id = form.save().pk
                contact = Products.objects.get(pk=id)
                if files:
                    for f in files:
                        fl = Files(contact=contact, file=f)
                        fl.save()
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                return HTTPResponse(form.errors)

        form = AddproductFrom()
        return render(request, 'main/forms/addproduct.html', {'form': form})
    
    else:
        return redirect('home-page')


def addEmail(request):
    if request.method == 'POST':
        form = EmailInput(request.POST)
        if form.is_valid():
            form.save()

    return redirect(request.META.get('HTTP_REFERER'))


def feedback(request):
    if request.method == 'POST':
        name = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_mail = request.POST.get('from_mail', '') 
        
        send_mail(name, message, from_mail, [
                  'msd2007msd02@gmail.com'], fail_silently=False,)
        return redirect(request.META.get('HTTP_REFERER'))


def like(request, p_id):
    if request.user.is_authenticated:
        if not request.session.get('liked'):
            request.session['liked'] = list()
        else:
            request.session['liked'] = list(request.session['liked'])

        data = {'id': p_id}
        request.session['liked'].append(data)
    else:
        messages.add_message(request,  messages.ERROR,
                            'You need to log in to like products!!!')
    return redirect(request.META.get('HTTP_REFERER'))


def unlike(request, p_id):
    if request.user.is_authenticated:
        if not request.session.get('liked'):
            request.session['liked'] = list()
        else:
            request.session['liked'] = list(request.session['liked'])
        prod_lst = request.session['liked']
        
        
        for it in prod_lst:
            if str(it['id']) == str(p_id):
                request.session['liked'].remove(it)

        return redirect(request.META.get('HTTP_REFERER'))


class SearchResult(ListView):
    paginate_by = 8
    model = Products
    template_name = 'main/search.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super(SearchResult, self).get_context_data(**kwargs)
        context['search_qw'] = self.request.GET.get('q')

        url = self.request.get_full_path()
        if '&' in url:
            url = '&'.join(url.split('&')[:-1])
        context['url'] = url 


        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Products.objects.filter(status='Published').filter(
            Q(prod_name__iregex=query) 
        )

        return object_list


class FilterProducts(FilterView):
    paginate_by = 8
    model = Products
    template_name = 'main/cotalog-base.html'
    context_object_name = 'products'
    filterset_class = ProductFilter

    def get_context_data(self, **kwargs):
        context = super(FilterProducts, self).get_context_data(**kwargs)
        context['img'] = Files.objects.all()
        context['categories'] = Categories.objects.all()
        context['filtered'] = True
        ctg_id = self.request.GET.get('category')
        category = Categories.objects.get(id=ctg_id)
        post_ctg = PostCategories.objects.filter(category=category)
        post_id = ''
        if self.request.GET.get('post_category') != '':
            post_id = int(self.request.GET.get('post_category'))

        context['form_data'] = {
            'min': self.request.GET.get("price_min"),
            'max': self.request.GET.get("price_max"),
            'ctg': int(self.request.GET.get('category')),
            'post_ctg': post_ctg,
            'post_id': post_id
        }

        url = self.request.get_full_path().split('&')
        if 'page=' in url[-1]:
            url = url[:-1]
            print(url)
        context['url'] = '&'.join(url) + '&'

        return context

    def get_queryset(self):
        return Products.objects.filter(status='Published').all()


def get_postcat(request, id):
    categ = Categories.objects.get(id=id)
    post_cat = PostCategories.objects.filter(category=categ)
    data = {}

    post_categ = {it.post_category: it.id for it in post_cat}
    atributs = {
        atr.name: {option.id: option.name for option in atr.parametrs.all()}

        for atr in categ.atributs.all()
    }
    data['post_ctg'] = post_categ
    data['atributs'] = atributs

    return JsonResponse(data, safe=False)


def get_atributs(request):
    prod_id = request.POST.get('id')
    prod = Products.objects.get(id=prod_id)
    prod_atrs = prod.category.atributs.all()
    prod_var = Products.objects.get(id=prod_id).variant.first()
    atributs = {
        atr.name: {option.id: option.name for option in atr.parametrs.all()}

        for atr in prod_atrs
    }
    choosen = [option.id for option in prod_var.atribut.all()]

    data = {
        'atr': atributs,
        'lst': choosen
    }

    print(atributs)
    
    print(prod_var.atribut.all())


    return JsonResponse(data, safe=False)


def faq(request):
    faq = FAQ.objects.all()
    return render(request, 'main/faq-pages/faq.html', {"faqs": faq})

    


def ship_and_returns(request):
    return render(request, 'main/faq-pages/ship.html')


def shop_policy(request):
    return render(request, 'main/faq-pages/policy.html')


@user_passes_test(lambda u: u.is_superuser)
def newsletter_page(request):
    if request.method == 'POST':
        text = request.POST['message']
        subject = request.POST['subject']
        subs = Subscribes.objects.all()
        for it in subs:
            send_mail(subject, text, 'dadamuhames@gmail.com', [it.email])


    return render(request, 'main/send_email.html')



def get_modal_data(request, p_id):
    product = Products.objects.filter(status='Published').get(id=p_id)
    imgs = [get_thumbnailer(it.file)['product_img'].url for it in product.get_default().image.all()]
    total = product.get_default().price
    size = ''
    count = 1
    

    if not request.session.get('cart'):
        request.session['cart'] = list()
    else:
        request.session['cart'] = list(request.session['cart'])


    atributs = {}
    for atr in product.category.atributs.all():
        atributs[atr.name] = []
        for opt in atr.parametrs.all():
            atributs[atr.name].append({
                'name': opt.name,
                'id': opt.id
            })

    colors = []
    for color in product.colors.all():
        colors.append({
            'name': color.name,
            'id': color.id
        })

    data = {
        'variant': product.get_default().id,
        'name': product.prod_name,
        'price': product.get_default().price,
        'scu': product.id,
        'total': total,
        'count': count,
        'imgs': imgs,
        'atributs': atributs,
        'colors': colors
    }

    return JsonResponse(data, safe=False)

    
class ControlComments(ListView):
    paginate_by = 8
    model = Comments
    template_name = 'main/com_contr.html'
    context_object_name = 'comments'

    def get_queryset(self):
        return Comments.objects.filter(active=False).order_by('-id')


@user_passes_test(lambda u: u.is_superuser)
def accept_comment(request):
    comment_id = request.POST.get("comment_id")
    coment = Comments.objects.get(id=comment_id)
    url = request.POST.get('url')
    if '_del' in request.POST:
        coment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted')
    elif '_accept' in request.POST:
        coment.active = True
        coment.save()
        messages.add_message(request, messages.SUCCESS, 'Comment accepted')

    return redirect(url)


def page_not_found_view(request, *args, **argv):
    return render(request, 'main/404.html', status=404)


def page_not_found_view_500(request, *args, **argv):
    return render(request, 'main/404.html', status=500)


def get_variant(request):
    color_id = request.POST.get('color')
    color = Colors.objects.get(id=color_id)
    product = Products.objects.get(id=request.POST.get('id'))
    variants = product.variant.filter(color=color)

    for key in request.POST:
        if 'atribut_' in key:
            option = AtributParams.objects.get(id=request.POST.get(key))
            variants = variants.filter(atribut=option)

    data = {}
    if variants.count() > 0:
        variant = variants.first()
        in_cart = str(variant.id) in [str(item['product_variant']) for item in request.session.get('cart', list()) if item['active'] == 'True']

        data =  {
            'id': variant.id,
            'price': variant.price,
            'qty': variant.qty,
            'in_cart': in_cart,
            'img': [get_thumbnailer(img.file)['prod_photo'].url for img in variant.image.all()]
        }
        

    return JsonResponse(data, safe=False)


def CartDeteilView(request, pk):
    items = [it for it in request.session.get('cart') if str(it['product_variant']) == str(pk)]

    if len(items) == 0:
        return redirect('home-page')

    prod = Products.objects.get(id=str(items[0]['product']))
    
    cart_item = {
        'product': prod,
        'variant': ProductVariants.objects.get(id=str(items[0]['product_variant'])),
        'price': items[0]['price'],
        'qty': items[0]['count'],
    }

    liked  = str(items[0]['product']) in [str(wish['id']) for wish in request.session.get('liked', list())]
    comment_input = Comment(initial={'product': prod})
    comments = Comments.objects.filter(product=prod).filter(
        active=True).filter(parent=None).order_by('-id')
    answers = Comments.objects.filter(product=prod).filter(active=True).exclude(parent=None)

    data = {
        'cart_item': cart_item,
        'liked': liked,
        'comment_input': comment_input,
        'comments': comments,
        'answers': answers
    }


    return render(request, 'main/cart-view.html', data)


'''            if request.user.is_authenticated:
                try:
                    cart = Cart.objects.filter(
                        owner=request.user).filter(active=True).get(product=prod)
                    cart.size = size
                    cart.quantity = qunt
                    cart.save()
                except:
                    cart = Cart(owner=owner, product=prod, size=size, quantity=qunt, active=True)
                    cart.save()
                    messages.add_message(request,  messages.SUCCESS, 'Seccsesfuly added to your cart')
            else:
    if request.user.is_authenticated:
        for it in Cart.objects.filter(owner=request.user).filter(active=False):
            it.delete()
    else:                


'''
