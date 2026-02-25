from rest_framework import serializers

from .models import AudioFile


class UploadAudioSerializer(serializers.Serializer):
    file = serializers.FileField(help_text="Audio file to upload")


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
        request = self.context.get("request")
        if request and obj.file:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url if obj.file else None
