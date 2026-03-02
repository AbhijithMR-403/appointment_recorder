from celery import shared_task
from django.utils import timezone
from datetime import timedelta

from audio_core.models import AudioFile


@shared_task
def delete_old_audio_files():
    """
    Delete audio files from media (storage) for records created more than 24 hours ago,
    and mark those records as deleted=True in the database.
    """
    cutoff = timezone.now() - timedelta(hours=24)
    old_files = AudioFile.objects.filter(created_at__lt=cutoff, deleted=False)

    count = 0
    for audio_file in old_files:
        # Delete the file from media (storage)
        if audio_file.file:
            try:
                audio_file.file.delete(save=False)
            except Exception:
                pass
        audio_file.deleted = True
        audio_file.save(update_fields=["deleted"])
        count += 1

    return count
