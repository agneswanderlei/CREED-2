from django.apps import AppConfig


class OficiosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'oficios'

    def ready(self):
        import oficios.signals