# Django Notifications

## Описание
**Django Notifications** — это приложение для управления уведомлениями в Django. Оно позволяет отслеживать изменения в моделях и отображать уведомления в админ-панели.

## Установка

1. Установите пакет через `poetry` или `pip`:
   ```sh
   poetry add azzlem-django-notifications
   ```
   или
   ```sh
   pip install azzlem-django-notifications
   ```

2. Добавьте `django_notifications` в **INSTALLED_APPS** в `settings.py` (в начало списка):
   ```python
   INSTALLED_APPS = [
       "django_notifications",
       # другие приложения...
   ]
   ```

## Настройка

### 1. Добавление URL-маршрутов

В файле `urls.py` основного проекта добавьте маршрут для уведомлений:
   ```python
   from django.urls import path
   from django_notifications.views import get_notifications
   
   urlpatterns = [
       path("django_notifications/admin/notifications/", get_notifications, name="notifications"),
   ]
   ```

### 2. Настройка отслеживаемых моделей

В `settings.py` укажите модели, за которыми нужно следить:
   ```python
   TRACKED_MODELS = [
       "appname.ModelName",  # Замените на ваши модели
   ]
   ```

### 3. Подключение кастомной админки (если используется)

Если у вас кастомная админка, добавьте `CustomAdminSite`:
   ```python
   from django_notifications.admin import CustomAdminSite
   from django.contrib import admin
   
   class MyAdminSite(CustomAdminSite, admin.AdminSite):
       pass
   ```

## Использование
После настройки уведомления будут автоматически создаваться при изменении отслеживаемых моделей. Вы сможете просматривать их в админке по пути:
```
/admin/notifications/
```

## Лицензия
Проект распространяется под лицензией **MIT**.

---

📧 **Контакты:** Если у вас есть вопросы или предложения, пишите на [azzlem.sid@gmail.com](mailto:azzlem.sid@gmail.com).

