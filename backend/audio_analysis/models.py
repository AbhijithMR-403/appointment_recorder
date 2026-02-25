from django.db import models


class TranscriptionJobLog(models.Model):
    """Log entry for a Rev AI transcription job."""

    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "In progress"

    job_id = models.CharField(max_length=255, unique=True, db_index=True)
    media_url = models.URLField(max_length=2048)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
        db_index=True,
    )
    transcript = models.TextField(blank=True)
    failure_reason = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Transcription job log"
        verbose_name_plural = "Transcription job logs"

    def __str__(self):
        return f"{self.job_id} ({self.status})"
