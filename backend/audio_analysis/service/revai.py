"""
Rev AI Speech-to-Text API client.

Callback API: When submitting a job you can provide a notification_config.url
(webhook URL). Rev AI will POST to that URL when the job completes. Set
REV_AI_WEBHOOK_URL in settings for a default, or pass notification_url to
submit_job() per request.

Submits jobs and optionally polls/retrieves transcription results.
"""

import logging
from typing import Any, Optional

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

REV_AI_BASE_URL = "https://api.rev.ai/speechtotext/v1"
REV_AI_WEBHOOK_URL = "https://webhook.site/72500462-0db9-4cad-9e6e-8d85466b2fe3"

class RevAIClient:
    """Client for Rev AI Speech-to-Text API."""

    def __init__(
        self,
        access_token: Optional[str] = None,
        base_url: str = REV_AI_BASE_URL,
        notification_url: str = REV_AI_WEBHOOK_URL,
    ):
        self.base_url = base_url.rstrip("/")
        self.access_token = access_token or getattr(
            settings, "REV_AI_ACCESS_TOKEN", None
        )
        if not self.access_token:
            raise ValueError("Rev AI access token is required (REV_AI_ACCESS_TOKEN or pass access_token).")
        self.notification_url = notification_url
    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }

    def submit_job(
        self,
        media_url: str,
        timestamps: bool = False,
    ) -> dict[str, Any]:

        payload: dict[str, Any] = {
            "media_url": media_url,
            "options": {
                "timestamps": timestamps,
            },
        }
        if self.notification_url:
            payload["notification_config"] = {"url": self.notification_url}

        url = f"{self.base_url}/jobs"
        response = requests.post(
            url,
            headers=self._headers(),
            json=payload,
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
        logger.info("Rev AI job submitted: id=%s", data.get("id"))
        return data

    def get_job(self, job_id: str) -> dict[str, Any]:
        """Get status and details of a transcription job."""
        url = f"{self.base_url}/jobs/{job_id}"
        response = requests.get(url, headers=self._headers(), timeout=30)
        response.raise_for_status()
        return response.json()

    def get_transcript(self, job_id: str) -> str:
        """Get transcript result for a completed job (plain text)."""
        url = f"{self.base_url}/jobs/{job_id}/transcript"
        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {self.access_token}",
                "Accept": "text/plain",
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.text
