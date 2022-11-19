from distutils.command.upload import upload
from email.policy import default
from secrets import choice
from tokenize import blank_re
from urllib import request
from wsgiref.validate import validator
from django.db import models
from django.contrib.auth.models import User
from account.models import Profile
from easy_thumbnails.fields import ThumbnailerImageField
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from importlib import import_module
from django.core.validators import MaxValueValidator, MinValueValidator
from colorfield.fields import ColorField


class Colors(models.Model):
    name = models.CharField('Color Name', max_length=255)
    color = ColorField(default='#FF0000')

    def __str__(self):
        return self.name


class Atributs(models.Model):
    name = models.CharField('Atribut name', max_length=255)

    def __str__(self):
        return self.name


class AtributParams(models.Model):
    name = models.CharField('Param name', max_length=255)
    atr = models.ForeignKey(
        Atributs, on_delete=models.CASCADE, related_name='parametrs')


    def __str__(self):
        return self.atr.name + ' | ' + self.name

class Categories(models.Model):
    ctg_avatar = ThumbnailerImageField('Category Avatar', upload_to='ctg_image', null=True, blank=True)
    deskription = models.TextField('Deskription')
    category_name = models.CharField('Category name', max_length=100)
    atributs = models.ManyToManyField(Atributs, blank=True, null=True)

    def get_initial(self):
        return {'kt_ecommerce_add_category_meta_keywords' : [{'value': item.post_category} for item in self.post_ctg.all()]}

    def set_avatar(self):
        if not self.ctg_avatar:
            self.ctg_avatar = 'default-img.png'

    def __str__(self):
        return self.category_name


    def save(self, *args, **kwargs):
        self.set_avatar()
        super(Categories, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class PostCategories(models.Model):
    category = models.ForeignKey(Categories, blank=True, null=True, on_delete=models.CASCADE, related_name='post_ctg')
    post_category = models.CharField('Post Category', max_length=100)
 
    def __str__(self):
        return self.category.category_name + " : " + self.post_category

    class Meta:
        verbose_name = 'Post category'
        verbose_name_plural = 'Post categories'




# Create your models here.
class Products(models.Model):
    STATUS = [('Scheduled', 'Scheduled'), ('Inactive', 'Inactive'),
              ("Published", 'Published')]
    avatar = ThumbnailerImageField(upload_to='prod-imgs', default='default-img.png')
    prod_name = models.CharField('Product name', max_length=255, unique=True)
    deskription = models.TextField('Product description', max_length=1000)
    status = models.CharField('Status', max_length=255, choices=STATUS)
    information = models.TextField('Product details', max_length=800)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    post_category = models.ForeignKey(PostCategories, on_delete=models.CASCADE)
    colors = models.ManyToManyField(Colors)

    def get_absolute_url(self):
        return '/admin/products_edit/' + str(self.id)
    
    def get_default(self):
        return self.variant.get(default=True)
        
    def save_image(self):
        self.avatar = 'default-img.png'
            
    
    def save(self, *args, **kwargs):
        self.save_image()
        super(Products, self).save(*args, **kwargs)

    def __str__(self):
        return self.prod_name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


@receiver(post_delete, sender=Products)
def del_wishlist(sender, instance, **kwargs):
    request = HttpRequest()
    engine = import_module(settings.SESSION_ENGINE)
    session_key = 'liked'
    request.session = engine.SessionStore(session_key)
    if request.session.get('liked'):
        prod_lst = request.session['liked']

        for it in prod_lst:
            if str(it['id']) == str(instance.id):
                request.session['liked'].remove(it)


class ProductVariants(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='variant')
    default = models.BooleanField('Default', default=False)
    atribut = models.ManyToManyField(AtributParams)
    qty = models.PositiveIntegerField('Product quntity', default=1)
    color = models.ForeignKey(Colors, on_delete=models.CASCADE)
    price = models.FloatField('Price', validators=[MinValueValidator(1.00)])




class Files(models.Model):
    file = ThumbnailerImageField(upload_to='prod-imgs', blank=True, null=True)
    contact = models.ForeignKey(ProductVariants, blank=True, null=True, on_delete=models.CASCADE, related_name='image')

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"

    def __str__(self):
        return self.contact.product.prod_name



class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_cart')
    file = ThumbnailerImageField('Img', upload_to='cart_img', blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.FloatField('Total')
    quantity = models.IntegerField('Quantity', default='1')
    active = models.BooleanField('Active')

    def __str__(self):
        return self.product.prod_name

    def count_total(self):
        self.price = round(self.product.price * self.quantity, 2)

    def get_img(self):
        self.file = Files.objects.filter(contact=self.product).first().file

    def save(self, *args, **kwargs):
        self.count_total()
        self.get_img()
        super(Cart, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Cart item'
        verbose_name_plural = 'Cart items'


class Subscribes(models.Model):
    email = models.EmailField('Email', max_length=300)

    def __str__(self):
        return self.email


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField('Comment', max_length=1000)
    likes = models.IntegerField('Likes')
    active = models.BooleanField('Status', default=False)
    date = models.DateTimeField('Date')

    def profile(self):
        return Profile.objects.get(user=self.user)    

    def __str__(self):
        return self.user.username + self.product.prod_name + self.text

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'




