from django.shortcuts import render


def home(request):
    # Збираємо головну сторінку
    return render(request, 'index.html', {'title': 'Манікюрний салон - Головна'})


def other(request):
    # Збираємо іншу сторінку
    return render(request, 'other.html', {'title': 'Наші послуги'})

