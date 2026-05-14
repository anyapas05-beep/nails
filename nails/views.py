from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Avg
from django.core.mail import send_mail
from django.http import JsonResponse
from .models import Product, Category, Brand, Review, Newsletter


# --- КАТАЛОГ ТА ТОВАРИ ---

def catalog_view(request):
    """Відображення каталогу з фільтрацією"""
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()

    category_id = request.GET.get('category')
    if category_id and category_id.isdigit():
        products = products.filter(category_id=category_id)

    selected_brands = [b for b in request.GET.getlist('brand') if b.isdigit()]
    if selected_brands:
        products = products.filter(brand_id__in=selected_brands)

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'selected_brands_ids': [int(b) for b in selected_brands],
    }
    return render(request, 'catalog.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    brands = Brand.objects.all()

    return render(request, 'category.html', {
        'category': category,
        'products': products,
        'brands': brands
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST' and 'rating' in request.POST:
        rating_value = request.POST.get('rating')
        if rating_value:
            Review.objects.create(product=product, rating=float(rating_value))
            messages.success(request, "Дякуємо за вашу оцінку!")
            return redirect('product_detail', pk=product.pk)

    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    return render(request, 'product_detail.html', {
        'product': product,
        'average_rating': round(average_rating, 1),
    })


# --- ЛОГІКА КОШИКА (СЕСІЇ + AJAX) ---

def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['cart'] = cart
    request.session.modified = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'ok',
            'cart_count': sum(cart.values())
        })

    messages.success(request, "Товар додано в кошик!")
    return redirect('cart_detail')


def cart_detail(request):
    cart_session = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart_session.items():
        product = Product.objects.filter(id=product_id).first()
        if product:
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'item_total': item_total,
            })

    return render(request, 'cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart_detail')


# --- ОФОРМЛЕННЯ ЗАМОВЛЕННЯ ---

def checkout_view(request):
    """Сторінка з формою оформлення (Крок 1 та 2)"""
    cart_session = request.session.get('cart', {})
    if not cart_session:
        return redirect('catalog')

    total_price = 0
    cart_items = []
    for product_id, quantity in cart_session.items():
        product = Product.objects.filter(id=product_id).first()
        if product:
            item_total = product.price * quantity
            total_price += item_total
            cart_items.append({'product': product, 'quantity': quantity, 'total': item_total})

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


def checkout_complete(request):
    cart_session = request.session.get('cart', {})
    if not cart_session:
        return redirect('catalog')

    # Отримуємо email з POST-запиту (з форми оформлення)
    customer_email = request.POST.get('email')
    customer_name = request.POST.get('first_name', 'Клієнт')

    if customer_email:
        total_price = 0
        items_summary = ""
        for product_id, quantity in cart_session.items():
            product = Product.objects.filter(id=product_id).first()
            if product:
                items_summary += f"- {product.name} ({quantity} шт.)\n"
                total_price += product.price * quantity

        subject = 'LumiNail — Ваше замовлення прийнято!'
        message = f"Вітаємо, {customer_name}!\n\nДякуємо за замовлення в нашому магазині.\n\n" \
                  f"Ваші товари:\n{items_summary}\n" \
                  f"Загальна сума: {total_price} грн.\n\n" \
                  f"Ми зв'яжемося з вами для підтвердження доставки по м. Луцьк."

        try:
            send_mail(subject, message, 'lumi.nail.lutsk@gmail.com', [customer_email])
        except Exception as e:
            print(f"Помилка пошти: {e}")

    # Очищення кошика
    request.session['cart'] = {}
    request.session.modified = True
    return render(request, 'checkout_success.html')

# --- СЕРВІСИ ТА ІНШЕ ---

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            obj, created = Newsletter.objects.get_or_create(email=email)
            if created:
                try:
                    send_mail(
                        'LumiNail — Підписка підтверджена!',
                        'Вітаємо! Ви успішно підписалися на розсилку LumiNail у м. Луцьк.',
                        'vash_email@gmail.com',
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, "Лист із підтвердженням відправлено!")
                except Exception as e:
                    messages.error(request, f"Помилка відправки: {e}")
            else:
                messages.info(request, "Ви вже підписані на наші новини.")

    return redirect(request.META.get('HTTP_REFERER', 'catalog'))


def about_view(request):
    return render(request, 'about.html')


def shipping_view(request):
    return render(request, 'shipping.html')


def contacts_view(request):
    return render(request, 'contacts.html')