"""
Transcription via Rev AI.

Submit a job and log it; transcript or failure is delivered via webhook callback.
"""

import logging

from openai import OpenAI

from .service.openai import OpenAISummarizer

from .models import TranscriptionLog
from .service.revai import RevAIClient
from ghl_integration.models import Contact

logger = logging.getLogger(__name__)


class TranscriptionService:
    """Transcribe audio via Rev AI (callback-based)."""

    @staticmethod
    def transcribe(
        media_url: str,
        contact: Contact,
        access_token: str | None = None,
        audio_file=None,
    ) -> str:
        """Submit a transcription job. Result comes via webhook callback."""
        client = None
        if not access_token:
            client = RevAIClient()
        else:
            client = RevAIClient(access_token=access_token)
        job = client.submit_job(media_url=media_url, timestamps=False)
        job_id = job["id"]

        TranscriptionLog.objects.create(
            job_id=job_id,
            media_url=media_url,
            status=TranscriptionLog.Status.IN_PROGRESS,
            contact=contact,
            audio_file=audio_file,
        )

        return job_id


def summarize_transcription(
    transcription_text: str,
    openai_client: OpenAI | None = None,
    initial_prompt: str | None = None,
) -> str:
    """
    Function wrapper around OpenAISummarizer for backward-compatible use.
    """
    summarizer = OpenAISummarizer(openai_client=openai_client)
    return summarizer.summarize(
        transcription_text=transcription_text,
        initial_prompt=initial_prompt,
    )
