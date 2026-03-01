import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import TranscriptionLog
from .tasks import analyze_transcription_task


def _rev_status_to_log_status(rev_status):
    if rev_status == "transcribed":
        return TranscriptionLog.Status.TRANSCRIBED
    if rev_status == "failed":
        return TranscriptionLog.Status.FAILED
    return TranscriptionLog.Status.IN_PROGRESS


@method_decorator(csrf_exempt, name="dispatch")
class RevCallbackView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        # Rev sends job as root object (no "job" wrapper)
        job_data = data.get("job", data)

        job_id = job_data.get("id")
        if not job_id:
            return JsonResponse({"success": False, "error": "Missing job id"}, status=400)

        rev_status = job_data.get("status", "")
        media_url = job_data.get("media_url", "")
        failure = job_data.get("failure", "") or job_data.get("failure_detail", "")

        try:
            log = TranscriptionLog.objects.get(job_id=job_id)
        except TranscriptionLog.DoesNotExist:
            # We can't create a TranscriptionLog here because `contact` is required.
            # Returning 200 prevents Rev from retrying endlessly for unknown jobs.
            return JsonResponse(
                {"success": False, "error": f"Unknown job id: {job_id}"},
                status=200,
            )

        log.media_url = media_url or log.media_url
        log.status = _rev_status_to_log_status(rev_status)
        log.failure_reason = failure
        log.save(update_fields=["media_url", "status", "failure_reason", "updated_at"])

        if rev_status == "transcribed":
            try:
                analyze_transcription_task.delay(job_id)
            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)}, status=400)
        return JsonResponse(
            {"success": True, "action": "updated", "job_id": job_id}
        )
