from django.shortcuts import render, redirect

from django_notifications.models import Notification


def get_notifications(request):
    notification = Notification.objects.filter(ident=True).first()
    if not notification:
        return redirect('http://127.0.0.1:8000/admin/')
    url = f"http://127.0.0.1:8000/admin/{notification.app_name_ident}/{notification.app_name_model}/{notification.app_id_object}/change/"

    notification.ident = False
    notification.save()
    return redirect(url)
