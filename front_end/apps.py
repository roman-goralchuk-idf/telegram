from django.apps import AppConfig


class FrontEndConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'front_end'

    BOOTSTRAP5 = {
        "css_url": {},  # I could add a custom URL here
        "theme_url": "..."  # Or I could override the theme here
    }
