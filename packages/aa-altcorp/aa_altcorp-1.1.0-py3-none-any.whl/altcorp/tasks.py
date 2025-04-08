"""
Tasks
"""

# Third Party
from celery import shared_task
from dhooks_lite import Embed
from discord import Color

# Django
from django.db import transaction

# Alliance Auth
from allianceauth.eveonline.models import EveAllianceInfo, EveCorporationInfo
from allianceauth.services.hooks import get_extension_logger

from .app_settings import AC_ALT_ALLIANCE, AC_IGNORE_CORPS
from .helpers import member_tokens_count_for_corp, send_embed_message
from .models import AltCorpRequest

logger = get_extension_logger(__name__)


def process_existing_requests(existing_requests, corp_ids_in_alliance):
    """Process approved and effective AltCorpRequest entries."""
    non_compliant_corps = []
    revoke_corps = []

    for altcorp in existing_requests:
        if altcorp.corporation.corporation_id in corp_ids_in_alliance:
            tokens = member_tokens_count_for_corp(altcorp.corporation.corporation_id)

            if altcorp.status == AltCorpRequest.RequestStatus.APPROVED:
                altcorp.mark_effective()
            elif altcorp.status == AltCorpRequest.RequestStatus.EFFECTIVE:
                handle_compliance(altcorp, tokens, non_compliant_corps, revoke_corps)

    return non_compliant_corps, revoke_corps


def handle_compliance(altcorp, tokens, non_compliant_corps, revoke_corps):
    """Handle compliance checks and flagging."""
    if tokens < altcorp.corporation.member_count:
        if not altcorp.revoke_flag:
            altcorp.set_revoke_flag()
            send_non_compliance_alert(altcorp, tokens)

        if altcorp.revoke_flag and altcorp.is_revoke_deadline_passed():
            revoke_corps.append(altcorp.corporation.corporation_name)
            send_removal_alert(altcorp)
        else:
            non_compliant_corps.append(
                (altcorp.corporation.corporation_name, altcorp.revoke_deadline)
            )
    elif altcorp.revoke_flag:
        altcorp.clear_revoke_flag()


def send_non_compliance_alert(altcorp, tokens):
    """Send an alert for non-compliant corporations."""
    dead = altcorp.revoke_deadline.strftime("%B %d, %Y")
    desc = (
        f"This corp has {altcorp.corporation.member_count} members and only {tokens} tokens.\n"
        f"You have until **{dead}** to resolve the issue, or the corp will be removed from the alt alliance."
    )
    e = Embed(
        title=f"Corp {altcorp.corporation.corporation_name} uncompliant",
        description=desc,
        color=Color.yellow(),
    )
    send_embed_message(user=altcorp.user, embed=e)


def send_removal_alert(altcorp):
    """Send an alert when a corporation is being removed."""
    desc = (
        "This corp has failed to resolve compliance by the deadline.\n"
        "They will be removed from the alt alliance."
    )
    e = Embed(
        title=f"{altcorp.corporation.corporation_name} BEING REMOVED",
        description=desc,
        color=Color.red(),
    )
    send_embed_message(user=altcorp.user, embed=e)


@shared_task
def update_corp_requests_for_alliance():
    """Sync corporations in the specified alliance with the AltCorpRequest table."""
    logger.info(
        "Starting update_corp_requests_for_alliance for alliance ID: %d",
        AC_ALT_ALLIANCE,
    )
    try:
        ally = EveAllianceInfo.objects.get(alliance_id=AC_ALT_ALLIANCE)
        alliance_corps = (
            EveCorporationInfo.objects.filter(alliance=ally)
            .exclude(corporation_id__in=AC_IGNORE_CORPS)
            .values("corporation_id", "corporation_name", "member_count")
        )
        corp_ids_in_alliance = {corp["corporation_id"] for corp in alliance_corps}

        existing_requests = AltCorpRequest.objects.filter(
            corporation__corporation_id__in=corp_ids_in_alliance
        )
        existing_corp_ids = {
            request.corporation.corporation_id for request in existing_requests
        }

        with transaction.atomic():
            non_compliant_corps, revoke_corps = process_existing_requests(
                existing_requests, corp_ids_in_alliance
            )
            orphaned_requests = AltCorpRequest.objects.filter(
                corporation__corporation_id__in=(
                    existing_corp_ids - corp_ids_in_alliance
                )
            ).exclude(
                status__in=[
                    AltCorpRequest.RequestStatus.PENDING,
                    AltCorpRequest.RequestStatus.APPROVED,
                ]
            )
            if orphaned_requests.exists():
                orphaned_requests.delete()

        if non_compliant_corps or revoke_corps:
            embed_desc = ""
            if non_compliant_corps:
                embed_desc += "**Currently Non-Compliant Corps:**\n"
                embed_desc += (
                    "\n".join(
                        f"• {name} - Deadline: **{deadline.strftime('%B %d, %Y')}**"
                        for name, deadline in non_compliant_corps
                    )
                    + "\n\n"
                )
            if revoke_corps:
                embed_desc += "**Corps Pending Removal:**\n"
                embed_desc += "\n".join(f"• {name}" for name in revoke_corps)

            e = Embed(
                title="AltCorp Compliance Report",
                description=embed_desc,
                color=Color.orange(),
            )
            send_embed_message(True, embed=e)
    except (EveAllianceInfo.DoesNotExist, EveCorporationInfo.DoesNotExist) as e:
        logger.error(
            "Data retrieval failed for alliance %d: %s", AC_ALT_ALLIANCE, str(e)
        )
    except ValueError as e:
        logger.error("Value error encountered: %s", str(e))
    logger.info(
        "Finished update_corp_requests_for_alliance for alliance ID: %d",
        AC_ALT_ALLIANCE,
    )
