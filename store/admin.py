from django.contrib import admin

# Register your models here.
from store.models import Product, ProductGallery,Variations,ReviewRating
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model=ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified_date')
    prepopulated_fields = {'slug':('product_name',)}
    inlines = [ProductGalleryInline]


admin.site.register(Product, ProductAdmin)


class VariationsAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value')


admin.site.register(Variations, VariationsAdmin)
admin.site.register(ReviewRating)
admin.site.register(ProductGallery)