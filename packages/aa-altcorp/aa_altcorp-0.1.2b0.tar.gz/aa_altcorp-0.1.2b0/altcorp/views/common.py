"""
common
"""

# Alliance Auth
from allianceauth.eveonline.models import EveAllianceInfo

# Alt Corp
from altcorp.app_settings import AC_ALT_ALLIANCE
from altcorp.models import AltCorpRequest

DEFAULT_ICON_SIZE = 32


def add_common_context(
    request, context: dict  # pylint: disable=unused-argument
) -> dict:
    """adds the common context used by all view"""
    pending = AltCorpRequest.pending().count()
    danger = AltCorpRequest.danger().count()
    revoke = AltCorpRequest.expired_revoke_deadlines().count()
    try:
        alliance = EveAllianceInfo.objects.get(alliance_id=AC_ALT_ALLIANCE)
    except EveAllianceInfo.DoesNotExist:
        alliance = None

    if alliance:
        alliance_name = alliance.alliance_name
    else:
        alliance_name = "Unknown"
    new_context = {
        **{
            "total_count": {
                "pending": pending,
                "danger": danger,
                "revoke": revoke,
            },
            "alliance": alliance_name,
        },
        **context,
    }
    return new_context
