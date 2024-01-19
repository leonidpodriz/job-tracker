from django.conf import settings
from django.db import models


class ApplicationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"


class Application(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.PENDING,
    )
    notes = models.TextField(blank=True, null=True)

    class Meta:
        permissions = (
            ("change_application_status", "Can change application status"),
            ("change_application_notes", "Can change application notes"),
        )
