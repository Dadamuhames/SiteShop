from pyexpat.errors import messages
from urllib import request
from django.shortcuts import render, redirect
from django.views.generic import DetailView, ListView
import string
from .forms import RegistrForm
import random
from django.core.mail import send_mail
import myshop.settings as settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, ChangeBio, ChangeAcount
from main.models import Products, Cart, Files, Comments, Subscribes, ProductVariants
from .models import Profile
from django.contrib.auth.models import User, Group
from django.core import signing
from palpay.models import Orders, OrderedProducts
from django.contrib import messages
from django.contrib.messages import get_messages
from myshop import settings
# Create your views here.


def get_cart_items(request):
    final_lst = []
    if request.session.get('cart'):
        cart_items = [it for it in list(
            request.session.get('cart')) if it['active'] == 'True']
        for prods in cart_items:
            pd = Products.objects.get(id=str(prods['product']))
            variant = ProductVariants.objects.get(id=str(prods['product_variant']))
            final_lst.append({
                'variant': variant.id,
                'prim_key': pd.id,
                'name': pd.prod_name,
                'price': variant.price,
                'quant': prods['count'],
                'img': prods['file']['url'],
                'active': prods['active']
            })

    return final_lst

@login_required
def dashboard(request):
    prof = Profile.objects.get(user=request.user)
    default_data = prof.get_default_data()
    form = ChangeAcount(initial=default_data)
    comments_it = Comments.objects.filter(user=request.user).order_by('-id')
    errors = ''
    if request.session.get('prof_form_error'):
        errors = request.session.get('prof_form_error')
        del request.session['prof_form_error']

    final_lst = get_cart_items(request)
    total = 0
    for it in final_lst:
        total += float(it['price'])

    profile = Profile.objects.get(user=request.user)
    bio = ChangeBio(initial={'bio': profile.bio})

    if not request.session.get('liked'):
        request.session['liked'] = list()

    try:
        wish = request.session.get('liked')
        wish_final = [{'product': Products.objects.get(id=w['id'])} for w in wish]
    except:
        wish_final = []


    orders = Orders.objects.filter(user=request.user).exclude(status='Canseled').order_by('-id')
    order_products = OrderedProducts.objects.all()
    data = {
        'user': request.user,
        'cart': final_lst,
        'cart_count': len(final_lst),
        'prof': profile,
        'form': bio,
        'acc_form': form,
        'wish_list': wish_final[::-1],
        'total': total,
        'comments': comments_it,
        'orders': orders,
        'order_prod': order_products,
        'prof_errors': errors
    }
    return render(request, 'account/profile.html', data)


@login_required
def change_bio(request):
    if request.method == 'POST':
        form = ChangeBio(request.POST)
        if form.is_valid:
            bio = form.data['bio']
            prof = Profile.objects.get(user=request.user)
            prof.bio = bio
            prof.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def change_profile(request):
    if request.method == 'POST':
        form = ChangeAcount(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            inst = form.cleaned_data['instagram']
            tw = form.cleaned_data['twitter']
            fb = form.cleaned_data['facebook']
            wk = form.cleaned_data['wk']
            tel = form.cleaned_data['tel']


            user = User.objects.get(id=request.user.id)
            prof = Profile.objects.get(user=user)
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            prof.instagram = inst
            prof.facebook = fb
            prof.twitter = tw
            prof.wk = wk
            prof.tel = tel
            user.save()
            prof.save()
            return redirect(request.META.get('HTTP_REFERER'))

        else:
            request.session['prof_form_error'] = form.errors
            messages.add_message(request, messages.ERROR, 'Form is invalid')
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect(request.META.get('HTTP_REFERER'))


def generate_code():
    return random.randint(100000, 999999)


def sign_up(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            user_reg = RegistrForm(request.POST)
            code = ''
            if user_reg.is_valid():
                new_user = user_reg.save(commit=False)
                new_user.set_password(user_reg.cleaned_data['password1'])
                new_user.active = False
                
                name = user_reg.cleaned_data['username']
                email = user_reg.cleaned_data['email']
                Subscribes.objects.create(email=email)
                code = generate_code()
                message = f'Your verification code: {code}'
                send_mail(name, message, email, ['dadamuhames@gmail.com'])
                new_user.save()
                Group.objects.get(id=2).user_set.add(new_user)
                code = signing.dumps({'code': str(code)})
                return render(request, 'account/confirm.html', {'code': code, 'user': new_user})
            else:
                print(user_reg.errors)

        else:
            user_reg = RegistrForm()
            print(user_reg)

        return render(request, 'account/singup.html', {'form': user_reg})

    else:
        return render(request, 'account/alreadylogin.html')


@login_required
def confirm_pass(request, **kwargs):
    code = kwargs.get('code')
    id = kwargs.get('id')
    if request.method == 'POST':
        vf_code = request.POST.get('code')
        sended = signing.loads(code)['code']

        if vf_code == sended:
            user = User.objects.get(id=id)
            user.active = True
            user.save()
            
            return render(request, 'account/reg-done.html')
        else:
            pass

    return redirect('home-page')


def user_login(request):
    error = ''
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user = authenticate(
                    username=cd['username'], password=cd['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('profile')
                else:
                    error = 'Username or password is invalid.'
        else:
            form = LoginForm()

        return render(request, 'account/login.html', {'form': form, 'error': error})
    else:
        return render(request, 'account/alreadylogin.html')


class ViewProfiles(DetailView):
    model = User
    template_name = 'account/profile-base.html'
    context_object_name = 'user'

    def get(self, *args, **kwargs):

        if self.get_object() == self.request.user:
            return redirect('profile')

        else:
            self.model.objects.get(pk=kwargs['pk'])
            return super(ViewProfiles, self).get(request, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(ViewProfiles, self).get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=context['user'])
        context['comments'] = Comments.objects.filter(
            user=self.get_object()).order_by('-id')


        print(context['user'])
        return context


def chng_count(request):
    btn = request.POST.get('btn')
    p_id = request.POST.get('id')
    active = request.POST.get('active')
    print(active)
    #if request.user.is_authenticated:
    #    cart_it = Cart.objects.filter(owner=request.user).get(id=p_id)
    #    if btn == '_up':
    #        cart_it.quantity = int(cart_it.quantity) + 1
    #    elif btn == '_down' and int(cart_it.quantity) > 1:
    #        cart_it.quantity = int(cart_it.quantity) - 1
    #    cart_it.save()
    #else:
    if request.session.get("cart"):
        print('some text')
        print(p_id)
        print('ACtive', active)
        for it in list(request.session['cart']):
            print('1', it)
            if str(p_id) == str(it['product_variant']) and it['active'] == str(active):
                print(it)
                count = it['count']
                prod_price = ProductVariants.objects.get(id=it['product_variant']).price
                if btn == '_up':
                    it['count'] = int(count) + 1
                elif btn == '_down' and int(count) > 1:
                    it['count'] = int(count) - 1
                print(it['count'])
                it['price'] = int(count) * prod_price
                request.session.modified = True

    return redirect(request.META.get('HTTP_REFERER'))



def generate_pass():
    password = ''

    pass_len = random.randint(8, 20)
    alf_count = random.randint(pass_len//4, pass_len//2)
    nbm_count = pass_len - alf_count

    alf = string.ascii_uppercase
    nbm = string.digits

    for _ in range(alf_count):
        password += random.choice(alf)

    for _ in range(nbm_count):
        password += random.choice(nbm)

    password = list(password)
    random.shuffle(password)

    return ''.join(password)



def forgot_pass(request):
    error = 'Email'
    class_er = ''
    new_pass = generate_pass()
    if request.method == 'POST':
        email = request.POST['email']
        if email in [it.email for it in User.objects.all()]:
            
            user = User.objects.get(email=email)
            
            user.set_password(new_pass)
            user.save()

            message = f'We can\'t return you your password, so we give you a new one. New Password: {new_pass}'

            send_mail(user.username, message, settings.EMAIL_HOST_USER, [email])

            return render(request, 'account/check_your_email.html', {'email': email})
        else:
            error = 'There is no user with this email! Try again.'
            class_er = 'error'


    return render(request, 'account/forgot-pass.html', {'error': error, 'class': class_er})


@login_required
def pass_chng_done(request):
    return redirect('profile')


@login_required
def prof_img_change(request):
    if request.method == 'POST':
        if 'prof_img' in request.FILES:
            user = Profile.objects.get(user=request.user)
            user.prof_img = request.FILES['prof_img']
            user.save()
        else:
            messages.add_message(request, messages.ERROR, 'You don\'t choose the image')
    return redirect('profile')
