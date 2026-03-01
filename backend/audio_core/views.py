from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from audio_analysis.transcription import TranscriptionService
from ghl_integration.models import Contact

from .models import AudioFile
from .serializers import AudioFileSerializer, UploadAudioSerializer


class UploadAudioView(APIView):
    """POST: Upload an audio file and store in media folder."""

    def post(self, request):
        serializer = UploadAudioSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data["file"]
        contact_id = serializer.validated_data.get("contact_id")

        audio = AudioFile.objects.create(
            file=uploaded_file,
            filename=uploaded_file.name,
            file_size=uploaded_file.size,
            content_type=uploaded_file.content_type,
        )

        output_serializer = AudioFileSerializer(audio, context={"request": request})
        data = output_serializer.data

        try:    
            contact = Contact.objects.get(contact_id=contact_id)
            job_id = TranscriptionService.transcribe(
                media_url=data.get("file_url"),
                contact=contact,
            )
            data["transcription_job_id"] = job_id
        except Exception as exc:
            # If transcription fails to start, still return the uploaded audio info
            data["transcription_error"] = str(exc)

        return Response(data, status=status.HTTP_201_CREATED)


class AudioFileListView(APIView):
    """GET: List audio files (active and non-deleted only)."""

    def get(self, request):
        files = AudioFile.objects.filter(deleted=False, is_active=True).order_by("-created_at")
        serializer = AudioFileSerializer(files, many=True, context={"request": request})
        return Response({"count": len(serializer.data), "files": serializer.data})


