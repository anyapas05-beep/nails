# Додайте get_object_or_404 через кому після render
from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Brand


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


def category_detail(request, slug):
    # Відображаємо товари лише відповідної категорії
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    brands = Brand.objects.all()

    return render(request, 'category.html', {
        'category': category,
        'products': products,
        'brands': brands
    })


def product_detail(request, pk):
    # Отримуємо конкретний товар за його ID (pk)
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def about_view(request):
    return render(request, 'about.html')


def shipping_view(request):
    return render(request, 'shipping.html')


def contacts_view(request):
    return render(request, 'contacts.html')