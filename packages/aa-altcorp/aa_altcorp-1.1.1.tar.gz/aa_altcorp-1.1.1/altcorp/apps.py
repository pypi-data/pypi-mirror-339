# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

# Alt Corp
from altcorp import __version__


class AltcorpConfig(AppConfig):
    name = "altcorp"
    label = "altcorp"
    verbose_name = _(f"Alt Corp v{__version__}")
