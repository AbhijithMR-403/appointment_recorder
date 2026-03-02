from django.db import models


class TranscriptionLog(models.Model):
    """Log entry for a Rev AI transcription job."""

    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "In progress"
        TRANSCRIBED = "transcribed", "Transcribed"
        FAILED = "failed", "Failed"

    job_id = models.CharField(max_length=255, unique=True, db_index=True)
    media_url = models.URLField(max_length=2048)
    audio_file = models.ForeignKey(
        "audio_core.AudioFile",
        on_delete=models.CASCADE,
        related_name="transcription_logs",
        db_index=True,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
        db_index=True,
    )
    contact = models.ForeignKey(
        "ghl_integration.Contact",
        on_delete=models.CASCADE,
        related_name="transcription_logs",
        db_index=True,
    )
    transcript = models.TextField(blank=True, help_text="Full transcription of the audio.")
    summary = models.TextField(blank=True, help_text="Summary of the audio content.")
    failure_reason = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Transcription log"
        verbose_name_plural = "Transcription logs"

    def __str__(self):
        return f"{self.job_id} ({self.status})"
