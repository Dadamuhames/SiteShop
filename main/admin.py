from django.contrib import admin
from .models import Products, Files, Cart, Subscribes, Categories, PostCategories, Comments, AtributParams, Atributs, Colors, ProductVariants

# Register your models here.

class ProduсtsAdmin(admin.ModelAdmin):
    list_display = [it.name for it in Products._meta.fields]
    filter_horizontal = ('colors', )

    raw_id_fields = ['category', 'post_category']

    class Meta:
        modes = Products

admin.site.register(Products, ProduсtsAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = [it.name for it in Cart._meta.fields]

    class Meta:
        modes = Cart

admin.site.register(Cart, CartAdmin)



admin.site.register(Files)
admin.site.register(Subscribes)

class CtgAdmin(admin.ModelAdmin):
    list_display = [it.name for it in Categories._meta.fields]
    filter_horizontal = ('atributs', )

    class Meta:
        modes = Categories


admin.site.register(Categories, CtgAdmin)
admin.site.register(PostCategories)


class CommentsAdmin(admin.ModelAdmin):
    list_display = [it.name for it in Comments._meta.fields]

    class Meta:
        modes = Comments



admin.site.register(Comments, CommentsAdmin)



class AtributAdmin(admin.ModelAdmin):
    list_display = [it.name for it in Atributs._meta.fields]

    class Meta:
        modes = Atributs

admin.site.register(Atributs, AtributAdmin)


class AtributParamAdmin(admin.ModelAdmin):
    list_display = [it.name for it in AtributParams._meta.fields]

    class Meta:
        modes = AtributParams
admin.site.register(AtributParams, AtributParamAdmin)


class ColorAdmin(admin.ModelAdmin):
    list_display = [it.name for it in Colors._meta.fields]

    class Meta:
        modes = Colors


admin.site.register(Colors, ColorAdmin)


class AdminProdVar(admin.ModelAdmin):
    list_display = [it.name for it in ProductVariants._meta.fields]
    filter_horizontal = ('atribut', )

    class Meta:
        modes = ProductVariants
admin.site.register(ProductVariants, AdminProdVar)
