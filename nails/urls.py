from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_view, name='catalog'), # Головна сторінка тепер каталог
    path('about/', views.about_view, name='about'),
    path('shipping/', views.shipping_view, name='shipping'),
    path('contacts/', views.contacts_view, name='contacts'),
]