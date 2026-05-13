from django.shortcuts import render
from .models import Category, Product, Brand


def catalog_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    # 1. Фільтрація за категорією
    category_id = request.GET.get('category')
    if category_id and category_id.isdigit():
        products = products.filter(category_id=category_id)

    # 2. Фільтрація за брендами (кнопка "Застосувати")
    # Отримуємо список ID, ігноруючи порожні або некоректні значення
    selected_brands = [b for b in request.GET.getlist('brand') if b.isdigit()]

    if selected_brands:
        products = products.filter(brand_id__in=selected_brands)

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        # Передаємо список чисел для коректної перевірки чекбоксів у шаблоні
        'selected_brands_ids': [int(b) for b in selected_brands],
    }
    return render(request, 'catalog.html', context)


def about_view(request):
    return render(request, 'about.html')


def shipping_view(request):
    return render(request, 'shipping.html')


def contacts_view(request):
    return render(request, 'contacts.html')