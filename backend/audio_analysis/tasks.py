import logging

from celery import shared_task

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
    except Exception as e:
        logger.exception("Failed to summarize transcript for job %s: %s", job_id, e)
