from django.db import models


class Notification(models.Model):
    ident = models.BooleanField(default=True)
    app_name_model = models.TextField()
    app_name_ident = models.TextField()
    app_id_object = models.BigIntegerField(default=0)