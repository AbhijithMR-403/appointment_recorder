import logging

from celery import shared_task

from ghl_integration.models import GHLAuthCredentials
from ghl_integration.services import add_contact_note

from .models import TranscriptionLog
from .service.revai import RevAIClient
from .transcription import summarize_transcription

logger = logging.getLogger(__name__)


@shared_task
def analyze_transcription_task(job_id):
    """Fetch transcript from Rev AI and update TranscriptionLog."""
    try:
        log = TranscriptionLog.objects.get(job_id=job_id)
    except TranscriptionLog.DoesNotExist:
        logger.warning("TranscriptionLog job_id=%s not found", job_id)
        return

    try:
        client = RevAIClient()
        transcript = client.get_transcript(job_id)
    except Exception as e:
        logger.exception("Failed to fetch transcript for job %s: %s", job_id, e)
        log.status = TranscriptionLog.Status.FAILED
        log.failure_reason = str(e)
        log.save()
        return

    log.status = TranscriptionLog.Status.TRANSCRIBED
    log.transcript = transcript
    log.save()
    logger.info("Updated TranscriptionLog for job %s", job_id)

    try:
        summary = summarize_transcription(transcription_text=transcript)
        log.summary = summary
        log.save()
        logger.info("Summarized transcript for job %s", job_id)

        # Add summary as a note on the GHL contact
        contact = log.contact
        if contact and contact.contact_id and summary and contact.location_id:
            try:
                creds = GHLAuthCredentials.objects.filter(
                    location_id=contact.location_id
                ).first()
                if creds and creds.access_token:
                    add_contact_note(
                        contact_id=contact.contact_id,
                        body=summary,
                        access_token=creds.access_token,
                    )
                    logger.info(
                        "Added summary note to GHL contact %s for job %s",
                        contact.contact_id,
                        job_id,
                    )
                else:
                    logger.warning(
                        "No GHL credentials for location %s; skipping note for job %s",
                        contact.location_id,
                        job_id,
                    )
            except Exception as note_err:
                logger.exception(
                    "Failed to add summary note to GHL contact for job %s: %s",
                    job_id,
                    note_err,
                )
    except Exception as e:
        logger.exception("Failed to summarize transcript for job %s: %s", job_id, e)
