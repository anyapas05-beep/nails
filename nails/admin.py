from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, Brand, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Додаємо 'price' назад у list_display, щоб працював list_editable
    list_display = ('get_html_photo', 'name', 'brand', 'category', 'price', 'formatted_price', 'created_at')

    list_display_links = ('get_html_photo', 'name')
    search_fields = ('name', 'description')
    list_filter = ('category', 'brand', 'created_at')

    # Тепер 'price' є у list_display, і помилка зникне
    list_editable = ('price',)

    def get_html_photo(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=50 style='border-radius: 5px;'>")
        return "Немає фото"

    get_html_photo.short_description = "Мініатюра"

    def formatted_price(self, obj):
        return f"{obj.price} грн"

    formatted_price.short_description = "Ціна (гарна)"
    formatted_price.admin_order_field = 'price'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)