"""
Models
"""

# Django
from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now, timedelta
from django.utils.translation import gettext_lazy as _

# Alliance Auth
from allianceauth.eveonline.models import EveCorporationInfo
from allianceauth.services.hooks import get_extension_logger

from .app_settings import AC_REVOKE_DAYS

logger = get_extension_logger(__name__)


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        """Meta"""

        managed = False
        default_permissions = ()
        permissions = (
            ("access_app", "Can access this app and make a request"),
            ("manage_requests", "Can manage alt corp requests."),
        )


class AltCorpRequest(models.Model):
    """
    AltCorp Request
    """

    class RequestStatus(models.TextChoices):
        """
        Request Status
        """

        PENDING = "PENDING", _("Pending")
        APPROVED = "APPROVED", _("Approved")
        EFFECTIVE = "EFFECTIVE", _("Effective")
        REVOKED = "REVOKED", _("Revoked")

    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    corporation = models.ForeignKey(
        EveCorporationInfo,
        on_delete=models.CASCADE,
        related_name="alt_corp_requests",
        null=True,  # Allow nulls temporarily
        blank=True,
        help_text="The corporation associated with this request.",
    )
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=RequestStatus.choices, default=RequestStatus.PENDING
    )
    status_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date when the request was actioned (approved/revoked).",
    )
    revoke_flag = models.BooleanField(
        default=False, help_text="Flagged for removal due to token issues."
    )
    revoke_deadline = models.DateTimeField(
        null=True, blank=True, help_text="Deadline to resolve token issues."
    )

    def __str__(self):
        return f"{self.corporation.corporation_name} - {self.status}"

    # Business Logic Methods
    def mark_effective(self, date=None):
        """Mark the corporation as effective in the alliance."""
        self.status = self.RequestStatus.EFFECTIVE
        self.status_date = date or now()
        self.save()

    def mark_revoked(self):
        """Mark the corporation as revoked."""
        self.status = self.RequestStatus.REVOKED
        self.status_date = now()
        self.revoke_flag = False  # Clear revoke flag when revoked
        self.save()

    def set_revoke_flag(self):
        """Flag the corporation for revocation with a deadline."""
        self.revoke_flag = True
        self.revoke_deadline = now() + timedelta(days=AC_REVOKE_DAYS)
        self.save()

    def clear_revoke_flag(self):
        """Clear the revocation flag and deadline."""
        self.revoke_flag = False
        self.revoke_deadline = None
        self.save()

    def is_revoke_deadline_passed(self):
        """Check if the revoke deadline has passed."""
        return (
            self.revoke_flag and self.revoke_deadline and self.revoke_deadline < now()
        )

    # Query Methods (previously in the manager)
    @classmethod
    def pending(cls):
        """Return all requests with PENDING status."""
        return cls.objects.filter(status=cls.RequestStatus.PENDING)

    @classmethod
    def approved(cls):
        """Return all requests with APPROVED status."""
        return cls.objects.filter(status=cls.RequestStatus.APPROVED)

    @classmethod
    def effective(cls):
        """Return all requests with EFFECTIVE status."""
        return cls.objects.filter(status=cls.RequestStatus.EFFECTIVE)

    @classmethod
    def danger(cls):
        """Return all requests with revoke flag that haven't passed the revoke deadline."""
        return cls.objects.filter(revoke_flag=True, revoke_deadline__gt=now())

    @classmethod
    def revoked(cls):
        """Return all requests with REVOKED status."""
        return cls.objects.filter(status=cls.RequestStatus.REVOKED)

    @classmethod
    def expired_revoke_deadlines(cls):
        """Return all requests where the revoke deadline has passed."""
        return cls.objects.filter(revoke_flag=True, revoke_deadline__lt=now())
