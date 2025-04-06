from django.db.models.signals import post_save
from django.dispatch import receiver
from django_notifications.models import Notification
from django.conf import settings

TRACKED_MODELS = settings.TRACKED_MODELS


def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            app_name_model=instance._meta.model_name,
            app_name_ident=instance._meta.app_label,
            app_id_object=instance.id,
        )


# Динамически подписываем сигнал для каждой модели в TRACKED_MODELS
for model in TRACKED_MODELS:
    post_save.connect(create_notification, sender=model)


