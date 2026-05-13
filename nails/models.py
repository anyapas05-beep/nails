from django.db import models


# 1. Категорії товарів (напр. Лаки, Лампи, Інструменти)
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категорія")

    def __str__(self):
        return self.name


# 2. Бренди (напр. Kodi, Staleks, Komilfo)
class Brand(models.Model):
    name = models.CharField(max_length=100, verbose_name="Бренд")

    def __str__(self):
        return self.name


# 3. Товари для манікюру
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Бренд")

    name = models.CharField(max_length=150, verbose_name="Назва товару")
    description = models.TextField(verbose_name="Опис товару", blank=True, null=True)
    image = models.ImageField(upload_to='products/', verbose_name="Фото товару", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")

    # Автоматичні дати (вимога лаби)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Додано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    def __str__(self):
        return self.name