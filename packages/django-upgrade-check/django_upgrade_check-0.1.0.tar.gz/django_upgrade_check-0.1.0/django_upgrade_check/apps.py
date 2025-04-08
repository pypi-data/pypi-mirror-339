from django.apps import AppConfig


class DjangoUpgradeCheckConfig(AppConfig):
    name = "django_upgrade_check"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        from . import signals  # noqa
