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
]