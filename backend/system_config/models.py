from django.db import models


class SystemSettings(models.Model):

    # Open AI (summarization, etc.)
    openai_api_key = models.CharField(
        max_length=255,
        blank=True,
        help_text="OpenAI API key for summarization and other AI features.",
    )
    openai_model = models.CharField(
        max_length=64,
        default="gpt-4o-mini",
        help_text="Model name, e.g. gpt-4o-mini, gpt-4.",
    )

    # Rev AI (speech-to-text)
    rev_ai_access_token = models.CharField(
        max_length=255,
        blank=True,
        help_text="Rev AI access token for transcription.",
    )
    # Summarization
    summary_prompt = models.TextField(
        blank=True,
        default="Summarize the following transcript of an appointment or call. "
        "Include: main topics, decisions, action items, and any follow-up needed.",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "System settings"
        verbose_name_plural = "System settings"
        ordering = ["-created_at"]

    @classmethod
    def get_settings(cls) -> "SystemSettings":
        """Return the current settings (latest by created_at), creating with defaults if none exist."""
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj
