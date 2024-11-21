from django.apps import AppConfig


class BoardgamesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "boardgames"

    def ready(self):
        import boardgames.signals  # Import the signals module
