"""
Helper functions
"""

# Third Party
from dhooks_lite import Embed, Webhook
from discord import Embed as DiscordEmbed

# Django
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter
from allianceauth.framework.api.evecharacter import get_user_from_evecharacter
from allianceauth.services.hooks import get_extension_logger
from esi.models import Token

from .app_settings import AC_REQUIRED_SCOPES, AC_WEBHOOK, discord_bot_active

if discord_bot_active():
    # Third Party
    from aadiscordbot import tasks as bot_tasks  # pylint: disable=import-error


logger = get_extension_logger(__name__)


def member_tokens_count_for_corp(
    corp_id: int,
    quick_check: bool = True,
) -> tuple[int, list[str]]:
    """
    Returns the number of valid tokens for a given corp and a list of names without valid tokens.
    """
    members = EveCharacter.objects.filter(corporation_id=corp_id)
    invalid_names = []  # List to store names of members without valid tokens
    valid_count = 0  # Counter for valid tokens

    # Iterate over members and process each
    for member in members:
        if has_required_scopes_for_request(member, quick_check=quick_check):
            valid_count += 1  # Increment count if the token is valid
        else:
            invalid_names.append(
                member.character_name
            )  # Add name to the list if token is invalid
    return valid_count, invalid_names


def has_required_scopes_for_request(
    char: EveCharacter,
    quick_check: bool = True,
) -> bool:
    """Returns True if the given character has all required scopes, even across multiple tokens.

    Params:
    - char: EveCharacter object.
    - quick_check: if True, skips token validity checks to save time.
    """
    try:
        user = get_user_from_evecharacter(character=char)
        state_name = user.profile.state.name
    except ObjectDoesNotExist:
        return False

    if state_name not in AC_REQUIRED_SCOPES:
        return False

    required_scopes = set(AC_REQUIRED_SCOPES[state_name])

    token_qs = Token.objects.filter(character_id=char.character_id)
    if not quick_check:
        token_qs = token_qs.require_valid()

    # Accumulate all granted scope names across all tokens
    granted_scopes = set()
    for token in token_qs:
        granted_scopes.update(token.scopes.values_list("name", flat=True))

    # Check if all required scopes are present
    return required_scopes.issubset(granted_scopes)


def send_embed_message(
    webhook: bool = False, user: User = None, embed: Embed = None, cont: str = ""
):
    """Sends an embed message via webhook or user DM."""

    if webhook:
        hook = Webhook(
            AC_WEBHOOK,
            username="Alt Corp Alert",
        )
        hook.execute(embeds=[embed], content=cont)

    if user is not None:
        if discord_bot_active():
            e2 = DiscordEmbed.from_dict(embed.asdict())
            bot_tasks.send_message(user=user, embed=e2)
