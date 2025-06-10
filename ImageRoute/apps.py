from django.apps import AppConfig


class ImageRouteConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ImageRoute'

    def ready(self):
        # importujemy moduł, żeby zarejestrować sygnały
        import ImageRoute.signals
