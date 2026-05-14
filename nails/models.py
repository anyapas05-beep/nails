from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# 1. Категорії товарів
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категорія")

    def __str__(self):
        return self.name


# 2. Бренди
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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Додано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    def __str__(self):
        return self.name


# --- НОВІ МОДЕЛІ ДЛЯ ЛАБИ 7 ---

# 4. Модель для оцінювання та відгуків
class Review(models.Model):
    # Зв'язок з товаром: один товар може мати багато відгуків
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    # Оцінка від 1 до 5
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оцінка"
    )

    # Текст відгуку (можна залишити порожнім, якщо потрібна лише оцінка)
    comment = models.TextField(verbose_name="Коментар", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата відгуку")

    def __str__(self):
        return f"Оцінка {self.rating} для {self.product.name}"


# 5. Модель для збору Email (розсилка)
class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email для розсилки")
    subscribed_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата підписки")

    def __str__(self):
        return self.email