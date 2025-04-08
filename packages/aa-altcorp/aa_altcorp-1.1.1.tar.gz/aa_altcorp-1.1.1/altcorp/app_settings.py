"""App settings."""

# Django
from django.apps import apps
from django.conf import settings

# Alliance Auth
from app_utils.django import clean_setting


def discord_bot_active():
    """
    Check if discord bot is active
    :return: bool
    """
    if apps.is_installed("aadiscordbot"):
        # Third Party
        import aadiscordbot as ab  # pylint: disable=import-error, import-outside-toplevel

        version = ab.__version__.split(".")
        if int(version[0]) >= 3:
            return True
    return False


AC_WEBHOOK = clean_setting("AC_WEBHOOK", "", required_type=str)

# This is a map, where the key is the State the user is in
# and the value is a list of required scopes to check
AC_REQUIRED_SCOPES = getattr(
    settings,
    "AC_REQUIRED_SCOPES",
    {
        "Member": ["publicData"],
    },
)

# days after which a revoke request becomes actionable
AC_REVOKE_DAYS = clean_setting("AC_REVOKE_DAYS", 7, required_type=int)

# id of the alt alliance
AC_ALT_ALLIANCE = clean_setting("AC_ALT_ALLIANCE", None, required_type=int)

# characters belonging to these alliances are considered to be "in organization"
AC_ALLIANCE_IDS = clean_setting("AC_ALLIANCE_IDS", [], required_type=list)

# corps to ignore in alt alliance
AC_IGNORE_CORPS = clean_setting("AC_IGNORE_CORPS", [], required_type=list)
