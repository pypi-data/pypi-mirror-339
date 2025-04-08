"""
Manage requests view
"""

# Standard Library
from datetime import datetime

# Third Party
from dhooks_lite import Embed
from discord import Color

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Alliance Auth
from allianceauth.framework.api.user import get_main_character_from_user
from allianceauth.services.hooks import get_extension_logger
from app_utils.logging import LoggerAddTag

# Alt Corp
from altcorp import __title__
from altcorp.helpers import member_tokens_count_for_corp, send_embed_message
from altcorp.models import AltCorpRequest
from altcorp.views.common import add_common_context

logger = LoggerAddTag(get_extension_logger(__name__), __title__)


@login_required
@permission_required("altcorp.manage_requests")
def manage_requests(request):
    """
    Display the manage requests page with lists of approved,
    danger, and revoked alt corp requests.

    Retrieves lists of requests with approved, danger (revoke
    flag set and deadline not passed), and revoked statuses
    from the AltCorpRequest model. These lists are then passed
    to the template 'altcorp/manage_requests.html' to be rendered
    along with additional context information.
    """

    approved = AltCorpRequest.approved()
    danger = AltCorpRequest.danger()
    revoked = AltCorpRequest.revoked()
    context = {
        "approved": approved,
        "danger": danger,
        "revoked": revoked,
    }
    return render(
        request,
        "altcorp/manage_requests.html",
        add_common_context(request, context),
    )


def requests_list(request):
    """
    Get requests list
    """
    pending = AltCorpRequest.pending()
    corporations_data = []
    for corp in pending:
        tokens, unreg = member_tokens_count_for_corp(corp.corporation.corporation_id)
        main_character = get_main_character_from_user(user=corp.user)
        if corp.corporation.corporation_id == 98718236:
            tokens = corp.corporation.member_count
        row = {
            "ceo": main_character,
            "token_count": tokens,
            "unregistered": unreg,
            "request": corp,
        }
        corporations_data.append(row)
    corporations_data.sort(key=lambda x: (x["request"].corporation.corporation_name,))
    approved = AltCorpRequest.approved()
    corporations_data2 = []
    for corp in approved:
        tokens, unreg = member_tokens_count_for_corp(corp.corporation.corporation_id)
        main_character = get_main_character_from_user(user=corp.user)
        if corp.corporation.corporation_id == 98718236:
            tokens = corp.corporation.member_count
        row = {
            "ceo": main_character,
            "token_count": tokens,
            "unregistered": unreg,
            "request": corp,
        }
        corporations_data2.append(row)
    corporations_data2.sort(key=lambda x: (x["request"].corporation.corporation_name,))

    context = {"corps": corporations_data, "approved": corporations_data2}
    return render(
        request,
        "altcorp/partials/requests_list.html",
        context,
    )


def revocations_list(request):
    """
    Get revocations list
    """
    revoke = AltCorpRequest.expired_revoke_deadlines()
    corporations_data = []
    for corp in revoke:
        main_character = get_main_character_from_user(user=corp.user)
        row = {
            "ceo": main_character,
            "request": corp,
        }
        corporations_data.append(row)
    corporations_data.sort(key=lambda x: (x["request"].corporation.corporation_name,))
    danger = AltCorpRequest.danger()
    corporations_data2 = []
    for corp in danger:
        tokens, unreg = member_tokens_count_for_corp(corp.corporation.corporation_id)
        main_character = get_main_character_from_user(user=corp.user)
        row = {
            "ceo": main_character,
            "token_count": tokens,
            "unregistered": unreg,
            "request": corp,
        }
        corporations_data2.append(row)
    corporations_data2.sort(key=lambda x: (x["request"].corporation.corporation_name,))

    context = {"corps": corporations_data, "danger": corporations_data2}
    return render(
        request,
        "altcorp/partials/revocations_list.html",
        context,
    )


def manage_requests_write(request, request_id):
    """
    Approve/Reject a request
    """
    # approve request
    if request.method == "PUT":
        try:
            altcorp = AltCorpRequest.objects.get(id=request_id)
            altcorp.status = "APPROVED"
            altcorp.status_date = datetime.now()
            altcorp.save()
        except AltCorpRequest.DoesNotExist:
            return HttpResponseNotFound()

        desc = "Your alt corp application has been approved"
        e = Embed(
            title=f"{altcorp.corporation.corporation_name} Approved",
            description=desc,
            color=Color.green(),
        )
        send_embed_message(user=altcorp.user, embed=e)
        return HttpResponse("")
    # deny request
    if request.method == "DELETE":
        try:
            altcorp = AltCorpRequest.objects.get(id=request_id)
            desc = "Your alt corp application has been declined"
            e = Embed(
                title=f"{altcorp.corporation.corporation_name} Declined",
                description=desc,
                color=Color.red(),
            )
            send_embed_message(user=altcorp.user, embed=e)
            altcorp.delete()
        except AltCorpRequest.DoesNotExist:
            return HttpResponseNotFound()

        return HttpResponse("")

    return HttpResponseNotFound()
