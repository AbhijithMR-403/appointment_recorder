"""
Transcription via Rev AI.

Submit a job and log it; transcript or failure is delivered via webhook callback.
"""

import logging

from .models import TranscriptionLog
from .service.revai import RevAIClient

logger = logging.getLogger(__name__)


class TranscriptionService:
    """Transcribe audio via Rev AI (callback-based)."""

    @staticmethod
    def transcribe(media_url: str, access_token: str) -> str:
        """Submit a transcription job. Result comes via webhook callback."""
        client = RevAIClient(access_token=access_token)
        job = client.submit_job(media_url=media_url, timestamps=False)
        job_id = job["id"]

        TranscriptionLog.objects.create(
            job_id=job_id,
            media_url=media_url,
            status=TranscriptionLog.Status.IN_PROGRESS,
        )

        return job_id
