from django.contrib import admin

# Register your models here.
from cart.models import CartItem,CartModel


class CartModelAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'date_added')


class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'cart','quantity','is_active')


admin.site.register(CartModel,CartModelAdmin)
admin.site.register(CartItem,CartItemAdmin)