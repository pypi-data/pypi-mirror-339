from django.contrib import admin
from django_notifications.models import Notification
from django.contrib.admin import AdminSite


class CustomAdminMixin:
    def each_context(self, request):
        context = super().each_context(request)
        unread_notifications = Notification.objects.filter(ident=True).count() if request.user.is_authenticated else 0
        context['unread_notifications'] = unread_notifications
        return context


# Наследуемся от стандартного `AdminSite`, добавляя `Mixin`
class CustomAdminSite(CustomAdminMixin, AdminSite):
    pass


# Подменяем стандартный `admin.site`
admin.site.__class__ = CustomAdminSite
