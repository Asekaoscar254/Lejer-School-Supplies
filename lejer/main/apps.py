from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'
    verbose_name = 'Main'

    def ready(self):
        # Create the default groups if they don't exist. Guarded so migrations/imports don't fail.
        try:
            from django.contrib.auth.models import Group
            Group.objects.get_or_create(name='Admin')
            Group.objects.get_or_create(name='Staff')
        except Exception:
            # If DB isn't ready (migrations running), skip silently.
            pass
