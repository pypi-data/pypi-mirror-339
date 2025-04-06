from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_notifications"

    def ready(self):
        import django_notifications.signals
