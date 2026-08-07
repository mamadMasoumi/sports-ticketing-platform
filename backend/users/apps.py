from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Application configuration for user-related features.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
