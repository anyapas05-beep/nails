from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nails.urls')),  # Перенаправляємо всі запити у додаток nails
]