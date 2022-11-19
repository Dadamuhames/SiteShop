from django.contrib import admin
from .models import OrderedProducts, Orders, OrderHistory
# Register your models here.


class OrdersAdmin(admin.ModelAdmin):
    list_display = [it.name for it in Orders._meta.fields]

    class Meta:
        modes = Orders

admin.site.register(Orders, OrdersAdmin)


class OrderedProductsAdmin(admin.ModelAdmin):
    list_display = [it.name for it in OrderedProducts._meta.fields]

    class Meta:
        modes = OrderedProducts
        
admin.site.register(OrderedProducts, OrderedProductsAdmin)


class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = [it.name for it in OrderHistory._meta.fields]

    class Meta:
        modes = OrderHistory

admin.site.register(OrderHistory, OrderHistoryAdmin)
