from django.http import HttpResponse
from django.shortcuts import render

from category.models import Category
from store.models import Product, ReviewRating


def home(request):
    products = Product.objects.all().filter(is_available=True)
    categories = Category.objects.all()
    for product in products:
        review = ReviewRating.objects.filter(product_id=product.id)
    context = {
        'products':products,
        "categories": categories,
        "review":review
    }
    return render(request, "home.html",context)
