from multiprocessing import context
from urllib import request
from django.shortcuts import render, redirect
from main.models import Products, Files, Cart, Categories, PostCategories, Comments, Subscribes, Colors, ProductVariants, AtributParams, Atributs
from main.forms import AddproductFrom, AddToCart, EmailInput, Comment, ProductFilter
from account.models import Profile
from django.contrib import messages
from django.contrib.messages import get_messages
from .forms import EditProduct, AddCtg, FilterUsers, ProdVariantForm
from django.views.generic import DetailView, ListView, UpdateView, FormView, DeleteView, CreateView
from django.middleware.csrf import get_token
from palpay.models import Orders, OrderedProducts, OrderHistory
from palpay.forms import MakeOrder
import datetime
from PIL import Image
from account.forms import RegistrForm
from .models import FAQ
import os
from django_filters.views import FilterView
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from django.http import JsonResponse
from easy_thumbnails.files import get_thumbnailer

# Create your views here.
def open_main(request):
    return render(request, 'admins/dist/admin-base.html')


class ProductsView(ListView):
    model = Products
    template_name = 'admins/dist/apps/ecommerce/catalog/products.html'
    paginate_by = 8
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super(ProductsView, self).get_context_data(**kwargs)
        context['search_qw'] = self.request.GET.get('query')
        context['status'] = self.request.GET.get('status')
        url = self.request.path + '?'

        if '&' in self.request.get_full_path():
            url = self.request.get_full_path().split('&')
            if 'page=' in url[-1]:
                url = url[:-1]
            
            context['url'] = '&'.join(url) + '&'

            return context
        
        context['url'] = url
            

        return context

    def get_queryset(self,  **kwargs):
        if self.request.method == 'GET':
            if 'query' in self.request.GET and 'status' in self.request.GET:
                q = self.request.GET.get('query')
                status = self.request.GET.get('status')
                return Products.objects.filter(Q(status__iregex=status) & Q(prod_name__iregex=q))

            if 'query' in self.request.GET:
                q = self.request.GET.get('query')
                return Products.objects.filter(Q(prod_name__iregex=q))
            
            if 'status' in self.request.GET:
                status = self.request.GET.get('status')
                return Products.objects.filter(Q(status__iregex=status))
            

                    
        
        return Products.objects.all().order_by('-id')



class EditProductAdmin(UpdateView):
    model = Products
    form_class = EditProduct
    template_name = 'admins/dist/apps/ecommerce/catalog/edit-product.html'
    context_object_name = 'product'
    success_url = '/admin/products'

    def form_valid(self, form):
        id = form.save().pk
        prod = Products.objects.get(id=id)
        files = self.request.FILES.getlist('files')
        color_id = self.request.POST.get('colors')
        color = Colors.objects.get(id=color_id)
        atr_lst = []
        post = self.request.POST

        for key in self.request.POST:
            if 'atribut_' in str(key):
                atr_lst.append(post.get(key))

        prod_var = prod.variant.filter(default=True).first()
        prod_var.qty = self.request.POST.get('qty')
        prod_var.price = self.request.POST.get('price')
        prod_var.color = color 
        prod_var.atribut.set(atr_lst)
        prod_var.save()
        
        
        
        if files:
            for f in files:
                file = Files(contact=prod_var, file=f)
                file.save()
        return redirect("products-admin")


    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super(EditProductAdmin, self).get_context_data(**kwargs)
        context['colors'] = Colors.objects.all()   

        for atribut in context['product'].category.atributs.all():
            for option in atribut.parametrs.all():
               if option in context['product'].variant.first().atribut.all():
                    print(option)
               
        return context



def DeleteProducts(request, pk):
    Products.objects.get(id=pk).delete()
    return redirect(request.META.get("HTTP_REFERER"))

    
def del_products_image(request, pk):
    Files.objects.get(id=pk).delete()
    return redirect(request.META.get("HTTP_REFERER"))


class AddCateg(CreateView):
    model = Categories
    success_url = '/admin/categories'
    form_class = AddCtg
    template_name = 'admins/dist/apps/ecommerce/catalog/add-category.html'

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            id = form.save().pk
            ctg = Categories.objects.get(id=id)
            post_ctg_lst = form.cleaned_data['kt_ecommerce_add_category_meta_keywords']
            for post_ctg in post_ctg_lst:
                PostCategories.objects.create(category=ctg, post_category=post_ctg['value'])
        else:
            print(form.errors)

        return redirect('categories') 


class CategoriesView(ListView):
    model = Categories
    paginate_by = 10
    template_name = 'admins/dist/apps/ecommerce/catalog/categories.html'
    context_object_name = 'categories'

    def get_queryset(self):
        if self.request.method == 'GET':
            if 'query' in self.request.GET:
                q = self.request.GET.get('query')
                return Categories.objects.filter(Q(category_name__iregex=q))
        return Categories.objects.all().order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(CategoriesView, self).get_context_data(**kwargs)

        url = self.request.path + '?'

        if 'query=' in self.request.get_full_path():
            if '&' in self.request.get_full_path():
                url = self.request.get_full_path().split('&')[0] + '&'
            else:
                url = self.request.get_full_path() + '&'

        context['url'] = url

        return context


class EditCtg(UpdateView):
    model = Categories
    form_class = AddCtg
    template_name = 'admins/dist/apps/ecommerce/catalog/add-category.html'
    context_object_name = 'category'
    success_url = '/admin/categories'


    def get_initial(self):
        return self.get_object().get_initial()
        
    def form_valid(self, form):
        ctg = form.save(commit=False)
        ctg.category = form.cleaned_data['category_name']
        ctg.ctg_avatar = form.cleaned_data['ctg_avatar']
        ctg.save()
        if PostCategories.objects.filter(category=ctg):
            PostCategories.objects.filter(category=ctg).delete()
        post_ctg_lst = form.cleaned_data['kt_ecommerce_add_category_meta_keywords']
        for post_ctg in post_ctg_lst:
            PostCategories.objects.create(category=ctg, post_category=post_ctg['value'])

        return redirect("categories")



class AddProduct(CreateView):
    model = Products
    success_url = '/admin/products'
    form_class = EditProduct
    template_name = 'admins/dist/apps/ecommerce/catalog/edit-product.html'

    def form_valid(self, form):
        id = form.save().pk
        prod = Products.objects.get(id=id)
        files = self.request.FILES.getlist('files')
        color_id = self.request.POST.get('colors')
        print(color_id)
        color = Colors.objects.get(id=color_id)
        atr_lst = []
        post = self.request.POST

        for key in self.request.POST:
            if 'atribut_' in str(key):
                atr_lst.append(post.get(key))

        prod_var = ProductVariants(
            product=prod,
            default = True,
            color = color,
            qty = form.cleaned_data['qty'],
            price = form.cleaned_data['price']
        )
        prod_var.save()
        prod_var.atribut.set(atr_lst)
        
        prod.colors.add(prod_var.color)
        
        if files:
            for f in files:
                file = Files(contact=prod_var, file=f)
                file.save()
        return redirect("products-admin")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(AddProduct, self).get_context_data(**kwargs)
        context['type'] = 'Add'
        context['colors'] = Colors.objects.all()
        return context




class OrdersView(ListView):
    model = Orders
    paginate_by = 10
    template_name = 'admins/dist/apps/ecommerce/sales/listing.html'
    context_object_name = 'orders'

    def get_context_data(self, **kwargs):
        context = super(OrdersView, self).get_context_data(**kwargs)
        context['search_qw'] = self.request.GET.get('query')
        context['status'] = self.request.GET.get('status')
        url = self.request.path + '?'

        if '&' in self.request.get_full_path():
            url = self.request.get_full_path().split('&')
            if 'page=' in url[-1]:
                url = url[:-1]

            context['url'] = '&'.join(url) + '&'

            return context

        context['url'] = url

        return context

    def get_queryset(self,  **kwargs):
        if self.request.method == 'GET':
            if 'query' in self.request.GET and 'status' in self.request.GET and self.request.GET.get('status') != 'All':
                q = self.request.GET.get('query')
                status = self.request.GET.get('status')
                return Orders.objects.filter(Q(status__iregex=status) & (Q(user__username__iregex=q) | Q(id__iregex=q) | Q(user_name__iregex=q)))

            if 'query' in self.request.GET:
                q = self.request.GET.get('query')
                return Orders.objects.filter(Q(user__username__iregex=q) | Q(id__iregex=q) | Q(user_name__iregex=q))

            if 'status' in self.request.GET:
                status = self.request.GET.get('status')
                return Orders.objects.filter(Q(status__iregex=status))

        return Orders.objects.all().order_by('-id')


class OrderDeteils(UpdateView):
    model = Orders
    template_name = 'admins/dist/apps/ecommerce/sales/details.html'
    context_object_name = 'order'
    success_url = '#'
    fields = ['status']

    def form_valid(self, form):
        id = self.get_object().id
        form.save()
        status = form.cleaned_data['status']
        
        OrderHistory.objects.create(
            order = self.get_object(),
            status = status,
            comment = f'Order {status}',
            date = str(datetime.date.today())
        )

        return redirect(self.request.POST.get("url"))



def delete_order(request, pk):
    order = Orders.objects.get(id=pk)
    order.delete()
    return redirect('orders_listing')



class AddFaq(CreateView):
    model = FAQ
    success_url = '#'
    fields = ['question', 'answer']
    template_name = 'admins/dist/pages/faq/classic.html'

    def get_context_data(self, **kwargs):
        context = context = super(AddFaq, self).get_context_data(**kwargs)
        context['faq'] = FAQ.objects.order_by("-id")

        return context



class UsersList(ListView):
    model = User
    template_name = 'admins/dist/apps/user-management/users/list.html'
    context_object_name = 'users'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = context = super(UsersList, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        context['form'] = RegistrForm()
        context['search_qw'] = self.request.GET.get('query')
        url = self.request.path + '?'

        if '&' in self.request.get_full_path():
            url = self.request.get_full_path().split('&')
            if 'page=' in url[-1]:
                url = url[:-1]

            context['url'] = '&'.join(url) + '&'

            return context

        context['url'] = url



        return context

    def get_queryset(self,  **kwargs):
        if self.request.method == 'GET':
            if 'query' in self.request.GET and 'groups' in self.request.GET and self.request.GET.get('groups') != '':
                q = self.request.GET.get('query')
                groups = self.request.GET.get('groups')
                return User.objects.filter(Q(groups__id=groups) & (Q(username__iregex=q) | Q(email__iregex=q)))

            if 'query' in self.request.GET:
                q = self.request.GET.get('query')
                return User.objects.filter(Q(username__iregex=q) | Q(email__iregex=q))

            if 'groups' in self.request.GET:
                groups = self.request.GET.get('groups')
                return User.objects.filter(Q(groups__id=groups))

        return User.objects.all().all()


class UserDetails(UpdateView):
    model = User
    template_name = 'admins/dist/apps/user-management/users/view.html'
    context_object_name = 'user'
    success_url = '#'
    fields = ['username', 'email', 'first_name', 'last_name']


    def form_valid(self, form):
        form.save()
        print(self.request.FILES.get("avatar"))
        if self.request.FILES.get("avatar"):
            file = self.request.FILES.get("avatar")
            profile = Profile.objects.get(user=self.get_object())
            profile.prof_img = file
            profile.save()

        return redirect(self.request.POST.get("url"))

    def form_invalid(self, form):
        print(form.errors)
        return redirect(self.request.POST.get("url"))


    def get_context_data(self, **kwargs):
        context = super(UserDetails, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context


class RolesList(ListView):
    model = Group
    template_name = 'admins/dist/apps/user-management/roles/list.html'
    context_object_name = 'groups'

    def get_context_data(self, **kwargs):
        context = super(RolesList, self).get_context_data(**kwargs)

        context['perms'] = Permission.objects.all()
        context['perms_set'] = set([perm.content_type for perm in context['perms']])

        return context

    
def addGroup(request):
    if request.method == 'POST':
        perm_lst = []
        name = request.POST.get("group_name")

        if name in [group.name for group in Group.objects.all()]:
            messages.add_message(request,  messages.ERROR, 'Group name "{}" is unavialable'.format(name))
            return redirect("roles_list")


        if name:
            for key in request.POST:
                if key != 'csrfmiddlewaretoken' and key != 'group_name':
                    perm_lst.append(request.POST[key])

            new_gr = Group.objects.create(name=name)
            new_gr.permissions.set(perm_lst)
            new_gr.save()
        else:
            messages.add_message(request,  messages.ERROR, 'Form is invalid')
            return redirect("roles_list")

    return redirect("roles_list")

    

class UpdateRoles(UpdateView):
    model = Group
    template_name = 'admins/dist/apps/user-management/roles/view.html'
    context_object_name = 'group'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(UpdateRoles, self).get_context_data(**kwargs)

        context['perms'] = Permission.objects.all()
        context['perms_set'] = set(
            [perm.content_type for perm in context['perms']])

        return context


    def form_valid(self, form):
        group  = self.get_object()
        name = form.cleaned_data['name']
        perm_lst = []
        
        for key in self.request.POST:
            if key != 'csrfmiddlewaretoken' and key != 'name' and key != 'url':
                perm_lst.append(self.request.POST.get(key))

        group.permissions.set(perm_lst)
        group.name = name
        group.save()


        return redirect(self.request.POST.get("url"))


    def form_invalid(self, form):
        messages.add_message(self.request,  messages.ERROR,
                                'Form invalid')
        return redirect(self.request.POST.get("url"))



def del_user(request, pk):
    User.objects.get(id=pk).delete()
    return redirect("users_listing")


def change_group(request):
    if request.method == 'POST':
        form = request.POST
        user = User.objects.get(id=form.get("user"))
        url = form.get("url")
        group = Group.objects.get(id=form.get("user_role"))
        user.groups.clear()
        user.groups.add(group)

        return redirect(url)


def ceate_user(request):
    if request.method == 'POST':
        form = RegistrForm(request.POST)    
        if form.is_valid():
            user = form.save()
            if request.POST.get("user_role"):
                user.groups.add(request.POST.get("user_role"))
        else:
            print(form.errors)
            messages.add_message(request, messages.ERROR, 'Form is invalid')
            return redirect(request.META.get("HTTP_REFERER"))

        if not request.FILES.get("avatar"):
            return redirect("users_listing")


        file = request.FILES.getlist("avatar")[0]
        user.profile.prof_img = file
        user.profile.save()

    return redirect("users_listing")


def del_faq(request, pk):
    FAQ.objects.get(id=pk).delete()
    return redirect('FAQ')


def del_ctg(request, pk):
    Categories.objects.get(id=pk).delete()
    return redirect("categories")


def create_variant(request):
    if request.method == 'POST':
        form = ProdVariantForm(request.POST)
        var = form.save()

        files = request.FILES.getlist('files_inp')
        atr_lst = []
        for key in request.POST:
            if 'atribut_' in str(key):
                atr_lst.append(request.POST.get(key))

        var.atribut.set(atr_lst)
        var.save()

        if var.color not in var.product.colors.all():
            var.product.colors.add(var.color)

        if files:
            for f in files:
                file = Files(contact=var, file=f)
                file.save()

        return redirect(f'/admin/products_edit/{var.product.id}')




class CreateVariant(CreateView):
    model = ProductVariants
    template_name = 'admins/dist/apps/ecommerce/catalog/add-variant.html'
    form_class = ProdVariantForm


    def form_valid(self, form):
        var = form.save()
        files = self.request.FILES.getlist('files')
        atr_lst = []
        for key in self.request.POST:
            if 'atribut_' in str(key):
                atr_lst.append(self.request.POST.get(key))

        var.atribut.set(atr_lst)
        var.save()

        if var.color not in var.product.colors.all():
            var.product.colors.add(var.color)

        if files:
            for f in files:
                file = Files(contact=var, file=f)
                file.save()
        
        return redirect(f'/admin/products_edit/{var.product.id}')



    def get_context_data(self, **kwargs):
        context = super(CreateVariant, self).get_context_data(**kwargs)
        context['Add'] = True
        context['colors'] = Colors.objects.all()


        return context


def del_variant(request, pk):
    variant = ProductVariants.objects.get(id=pk)
    color = variant.color
    product = variant.product
    variant.delete()

    if product.variant.filter(color=color).count() == 0:
        lst = list(product.colors.all())
        lst.remove(color)
        product.colors.set(lst)
        

    return redirect(request.META.get('HTTP_REFERER'))


class UpdateVariant(UpdateView):
    model = ProductVariants
    form_class = ProdVariantForm
    template_name = 'admins/dist/apps/ecommerce/catalog/add-variant.html'
    context_object_name = 'variant'

    def form_valid(self, form):
        var = form.save()
        files = self.request.FILES.getlist('files')
        atr_lst = []
        for key in self.request.POST:
            if 'atribut_' in str(key):
                atr_lst.append(self.request.POST.get(key))

        var.atribut.set(atr_lst)
        var.save()

        if var.color not in var.product.colors.all():
            var.product.colors.add(var.color)

        if files:
            for f in files:
                file = Files(contact=var, file=f)
                file.save()

        return redirect(f'/admin/products_edit/{var.product.id}')


    def get_context_data(self, **kwargs):
        context = super(UpdateVariant, self).get_context_data(**kwargs)
        context['colors'] = Colors.objects.all()

        return context


def get_atribut(request):
    id = request.POST.get('id')
    atributs = Products.objects.get(id=id).category.atributs.all()

    data = {
       atr.name: {
            opt.id: opt.name
            for opt in atr.parametrs.all()
        }
        for atr in atributs
    }
    print(data)

    return JsonResponse(data, safe=False)