"""
create request view
"""

# Third Party
from dhooks_lite import Embed
from discord import Color

# Django
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import redirect, render

# Alliance Auth
from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo
from allianceauth.framework.api.user import get_main_character_from_user
from allianceauth.services.hooks import get_extension_logger

# Alt Corp
from altcorp.app_settings import AC_ALLIANCE_IDS
from altcorp.helpers import member_tokens_count_for_corp, send_embed_message
from altcorp.models import AltCorpRequest
from altcorp.views.common import add_common_context

logger = get_extension_logger(__name__)


@login_required
@permission_required("altcorp.access_app")
def index_view(request):
    """index page is used as dispatcher"""
    # app_count = (
    #     StandingRequest.objects.pending_requests().count()
    #     + StandingRevocation.objects.pending_requests().count()
    # )
    app_count = 0
    if app_count > 0 and request.user.has_perm("altcorp.manage_requests"):
        return redirect("altcorp:manage")

    return redirect("altcorp:create_requests")


@login_required
@permission_required("altcorp.access_app")
def create_requests(request):
    """
    Display main requests page
    """
    try:
        main_char_id = request.user.profile.main_character.character_id
    except AttributeError:
        main_char_id = None
    context = {
        "authinfo": {"main_char_id": main_char_id},
    }
    return render(
        request,
        "altcorp/create_requests.html",
        add_common_context(request, context),
    )


@login_required
@permission_required("altcorp.access_app")
def request_corporations(request):
    """
    Get corps that user can request for
    """
    user = request.user
    # get corps for user
    corporations = _calc_corporations(user)

    # now we need to take that list and get it ready for context
    # while checking the database for existing requests
    corporations_data = []
    for corp in corporations:
        # Try to fetch the related AltCorpRequest
        try:
            altcorp = AltCorpRequest.objects.get(corporation=corp)
            request_status = altcorp.status
            has_pending_revocation = altcorp.revoke_flag
            revocation_deadline = altcorp.revoke_deadline
            deadline_passed = altcorp.is_revoke_deadline_passed()
            # now we need to get the token count - that code is in the helpers
            tokens, unreg = member_tokens_count_for_corp(corp.corporation_id)
        except AltCorpRequest.DoesNotExist:
            # Default values if no request exists
            altcorp = None
            request_status = "None"
            has_pending_revocation = False
            revocation_deadline = ""
            deadline_passed = False
            tokens, unreg = member_tokens_count_for_corp(corp.corporation_id)

        # Gather data for this corporation
        row = {
            "token_count": tokens,
            "unregistered": unreg,
            "corp": corp,
            "status": request_status,
            "pending_revocation": has_pending_revocation,
            "revocation_deadline": revocation_deadline,
            "deadline_passed": deadline_passed,
            "altcorp": altcorp,
        }
        corporations_data.append(row)

    corporations_data.sort(key=lambda x: x["corp"].corporation_name)
    context = {"corps": corporations_data}
    return render(
        request,
        "altcorp/partials/request_corporations.html",
        context,
    )


@login_required
def request_corp_join(request: HttpRequest, corporation_id):
    """
    Request to join an alt alliance
    """
    # Fetch the corporation by ID
    corporation = EveCorporationInfo.objects.filter(
        corporation_id=corporation_id
    ).first()
    if not corporation:
        messages.warning(request, "Invalid corporation.")
        return redirect("altcorp:create_requests")

    # Check if a request already exists to avoid duplicates (optional)
    if AltCorpRequest.objects.filter(corporation=corporation).exists():
        messages.warning(
            request, "You have already submitted a join request for this corporation."
        )
    else:
        # Create a new request entry
        AltCorpRequest.objects.create(user=request.user, corporation=corporation)
        messages.success(request, "Your alt alliance join request has been submitted.")
        main_character = get_main_character_from_user(request.user)
        desc = f"{main_character} has submitted a join request for their alt corp: {corporation.corporation_name}"
        e = Embed(
            title=f"{corporation.corporation_name} join request",
            description=desc,
            color=Color.yellow(),
        )
        send_embed_message(True, embed=e)

    # Redirect to a relevant page (e.g., create_requests page)
    return redirect("altcorp:create_requests")


@login_required
def remove_corp_join(request: HttpRequest, altcorp_id: int):
    """
    Removes an AltCorpRequest by its ID.
    """
    # Attempt to fetch the request
    altcorp_request = AltCorpRequest.objects.filter(id=altcorp_id).first()

    if altcorp_request:
        # Delete the request if it exists
        altcorp_request.delete()
        messages.success(request, "The AltCorpRequest has been successfully removed.")
    else:
        # Handle the case where the request does not exist
        messages.error(request, "The specified request does not exist.")
    return redirect("altcorp:create_requests")


def _calc_corporations(user: User) -> list[EveCorporationInfo]:
    """
    Return corporation objects where the user's character is the CEO,
    excluding corporations in the specified alliances.

    Args:
        user (User): The user to check for corporations.

    Returns:
        List[EveCorporationInfo]: A list of corporation objects.
    """

    logger.debug("Starting _calc_corporations for user: %s", user.username)

    # Fetch all EveCharacters belonging to the user
    eve_characters_qs = EveCharacter.objects.filter(
        character_ownership__user=user
    ).select_related("character_ownership__user")

    character_ids = list(eve_characters_qs.values_list("character_id", flat=True))
    logger.debug("Found character IDs for user %s: %s", user.username, character_ids)

    if not character_ids:
        logger.warning(
            "No character IDs found for user '%s'. Returning an empty list.",
            user.username,
        )
        return []

    # Get the excluded alliance IDs from the configuration
    excluded_alliance_ids = AC_ALLIANCE_IDS
    logger.debug("Excluded alliance IDs: %s", excluded_alliance_ids)

    # Fetch corporations where the user's character is the CEO
    corporations_qs = EveCorporationInfo.objects.filter(
        ceo_id__in=character_ids
    ).exclude(alliance_id__in=excluded_alliance_ids)

    logger.debug(
        "Corporation queryset (before evaluation) for user '%s': %s",
        user.username,
        str(corporations_qs.query),
    )

    result = list(corporations_qs)
    logger.info(
        "Found %d corporation(s) for user '%s' after filtering.",
        len(result),
        user.username,
    )

    return result
