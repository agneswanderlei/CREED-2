from django.apps import AppConfig


class PresosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'presos'

    def ready(self):
        import presos.signals