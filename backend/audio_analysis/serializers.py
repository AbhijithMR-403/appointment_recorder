from rest_framework import serializers

from .models import TranscriptionLog


class TranscriptionLogSerializer(serializers.ModelSerializer):
    contact_id = serializers.CharField(source="contact.contact_id", read_only=True)

    class Meta:
        model = TranscriptionLog
        fields = [
            "id",
            "job_id",
            "media_url",
            "audio_file_id",
            "contact_id",
            "status",
            "transcript",
            "summary",
            "failure_reason",
            "created_at",
            "updated_at",
        ]
        read_only_fields = fields
