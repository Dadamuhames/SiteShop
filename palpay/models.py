from email.policy import default
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User, Group
from main.models import Cart, Products, ProductVariants
from django.contrib.sessions.models import Session
import datetime
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.validators import MinValueValidator

class Orders(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='order')
    user_name = models.CharField('Usernme', blank=True, null=True, max_length=255)
    session = models.CharField('Session Id', max_length=255, blank=True, null=True)
    name = models.CharField('Your name', max_length=255)
    order_img = ThumbnailerImageField(upload_to='order_img', blank=True, null=True)
    STATUS = [('Accepted', 'Accepted'), ('Performed', 'Performed'), ('Delivered', 'Delivered'), ('Canseled', 'Canseled')]
    CITYES = [('Ташкент', 'Ташкент'), ('Самарканд', 'Самарканд'), ('Бухара', 'Бухара'), ('Хива', 'Хива'),
    ('Шахрисабз', 'Шахрисабз'), ('Муйнак', 'Муйнак'), ('Заамин', 'Заамин'), ('Термез', 'Термез'), ('Гулистан', 'Гулистан'),
    ('Нукус', 'Нукус'), ('Наманган', 'Наманган'), ('Карши', 'Карши'), ('Навои', 'Навои'), ('Коканд', 'Коканд'), ('Андижан', 'Андижан'), ('Фергана', 'Фергана')]
    price = models.FloatField('Price')
    city = models.CharField('Country', max_length=255, choices=CITYES)
    adres = models.CharField('Your adress', max_length=255)
    your_number = models.CharField('Tel. number', max_length=13)
    cash = models.BooleanField('Pay with cash', default=True)
    payme = models.BooleanField('Pay by Payme',  default=False)
    email = models.EmailField("Email")
    date = models.DateTimeField('Date')
    item_count = models.IntegerField('Products Count', default=1)
    status = models.CharField('Status', max_length=255, choices=STATUS, default='Accepted')

    def set_data(self):
        self.date = str(datetime.datetime.now())

    
    def set_name(self):
        if not self.user:
            self.user_name = 'Anonimus User'


    def get_date_tire(self):
        d = self.date.day
        m = self.date.month
        y = self.date.year
        if int(d) < 10:
            d = '0' + str(d)
        if int(m) < 10:
            m = '0' + str(m)

        return f'{y}-{m}-{d}'

    def __str__(self):
        return 'Order' + ' ' + str(self.id)

    def save(self, *args, **kwargs):
        self.set_data()
        self.set_name()
        super(Orders, self).save(*args, **kwargs)


class OrderedProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='product')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariants, on_delete=models.CASCADE)
    img = ThumbnailerImageField(upload_to='order_products_img')
    size = models.CharField('Size', max_length=255)
    quantity = models.IntegerField('Quantity')
    total = models.FloatField('Total')

    def __str__(self):
        return self.order.__str__()



class OrderHistory(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='history')
    status = models.CharField("Status", max_length=255)
    comment = models.CharField("Comment", max_length=255)
    date = models.DateField("Update Date")

    def get_format_date(self):
        return f'{self.date.day}/{self.date.month}/{self.date.year}'

    def __str__(self):
        return str(self.order.id) + '' + self.status




class ShippingType(models.Model):
    name = models.CharField('Name', max_length=255)
    price = models.FloatField('Price', validators=[MinValueValidator(1.00)])
    img = ThumbnailerImageField(upload_to='shipping-img')

    def __str__(self):
        return self.name

        
