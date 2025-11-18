from django.conf import settings
from django.db import models
from django.utils import timezone

class UploadRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        COMPLETED_FAILED = "completed_failed", "Completed Failed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="upload_requests",
    )
    filename = models.CharField(max_length=255)
    url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    item_seq = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def mark_completed(self, url: str, item_seq: str = "") -> None:
        self.url = url
        self.status = self.Status.COMPLETED
        self.item_seq = item_seq
        self.completed_at = timezone.now()

    def mark_failed(self) -> None:
        self.status = self.Status.COMPLETED_FAILED
        self.completed_at = timezone.now()
