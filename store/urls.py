from django.urls import path
from . import views

urlpatterns = [
    path('', views.store,name='store'),
    path('category/<slug:category_slug>/', views.store,name='products_by_category'),
    path('category/<str:category_slug>/<str:product_slug>', views.ProductDetail.as_view(), name='product_details'),
    path('search/', views.search, name='search'),
    path('submit_review/<int:product_id>/',views.submit_review,name='submit_review')
]