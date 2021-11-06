from django.apps import AppConfig


class SifHubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sifhub'
    verbose_name = 'SifHub'

    def ready(self):
        from .signals import create_team
