from decouple import config
from rest_framework import serializers

from .models import AudioFile


class UploadAudioSerializer(serializers.Serializer):
    file = serializers.FileField(help_text="Audio file to upload")
    contact_id = serializers.CharField(required=False, allow_blank=False)


class AudioFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = AudioFile
        fields = [
            "id",
            "filename",
            "file_url",
            "file_size",
            "content_type",
            "created_at",
            "deleted",
            "is_active",
        ]
        read_only_fields = fields

    def get_file_url(self, obj):
        if obj.file:
            base_url = config("BASE_URL", default="").rstrip("/")
            return f"{base_url}{obj.file.url}" if base_url else obj.file.url
        return None
