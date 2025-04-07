from django.apps import AppConfig


class TumCommonXConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tum_common_x'
    verbose_name = 'TUM Common X'

    def ready(self):
        """
        Import signal handlers when the app is ready.
        """
        try:
            import tum_common_x.signals  # noqa
        except ImportError:
            pass 