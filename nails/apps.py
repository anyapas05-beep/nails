from django.apps import AppConfig


class NailsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nails'

    def ready(self):
        # Цей метод викликається один раз при запуску сервера.
        # Він імпортує файл із сигналами, щоб Django знав про розсилку.
        import nails.signals