from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views import View
from cart.models import CartItem
from cart.views import _cart_id
from category.models import Category
from store.models import Product


def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        "products": paged_products,
        "products_count": product_count,

    }

    return render(request, "store/store.html", context)


# def product_details(request,category_slug,product_slug):
#     return render(request,"store/product_detail.html")

#
class ProductDetail(View):
    def get(self, request, *args, **kwargs):
        category_slug = kwargs.get("category_slug")
        product_slug = kwargs.get("product_slug")
        product = Product.objects.get(slug=product_slug, is_available=True)
        is_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()

        context = {
            "product": product,
            "is_cart": is_cart,
        }
        return render(request, "store/product_detail.html", context)

# email not sending not used
# class SearchView(View):
#     def get(self,request,*args,**kwargs):
#         keyword = kwargs.get("keyword")
#         print(keyword)
#         return render(request, "store/store.html")
#
#     def post(self,request,*args,**kwargs):
#         keyword=kwargs.get("keyword")
#         return render(request, "store/store.html")
#
def search(request):
    if "keyword" in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'products_count': product_count
        }
    return render(request, "store/store.html", context)
