from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Product, Newsletter

@receiver(post_save, sender=Product)
def notify_subscribers(sender, instance, created, **kwargs):
    if created: # Тільки якщо товар створено вперше
        subscribers = Newsletter.objects.values_list('email', flat=True)
        if subscribers:
            send_mail(
                f'Новинка в LumiNail: {instance.name}!',
                f'У нашому магазині з’явився новий товар: {instance.name}.\nЦіна: {instance.price} грн.\nПоспішайте переглянути в каталозі!',
                'news@luminail.com',
                list(subscribers),
                fail_silently=False,
            )
