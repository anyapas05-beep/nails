from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_view, name='catalog'),
    # Додайте цей рядок:
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    path('about/', views.about_view, name='about'),
    path('shipping/', views.shipping_view, name='shipping'),
    path('contacts/', views.contacts_view, name='contacts'),
    # Маршрут для категорій (якщо потрібно для Лаби 6)
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout/complete/', views.checkout_complete, name='checkout_complete'),
]