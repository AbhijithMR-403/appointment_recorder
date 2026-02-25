import os
import uuid

import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

CONTENT_TYPE_TO_EXT = {
    "audio/mpeg": "mp3",
    "audio/mp3": "mp3",
    "audio/wav": "wav",
    "audio/x-wav": "wav",
    "audio/ogg": "ogg",
    "audio/webm": "webm",
    "audio/aac": "aac",
    "audio/flac": "flac",
    "audio/mp4": "m4a",
}


class DownloadError(Exception):
    """Raised when audio download fails."""

    def __init__(self, message, status_code=None):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class AudioDownloader:
    """Downloads audio from a URL and saves it to default storage."""

    def __init__(self, timeout=30):
        self.timeout = timeout

    def download_from_url(self, url, timeout=None):
        timeout = timeout if timeout is not None else self.timeout
        try:
            response = requests.get(url, timeout=timeout, stream=True)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise DownloadError("Request timed out while downloading the file.", status_code=408)
        except requests.exceptions.RequestException as e:
            raise DownloadError(f"Failed to download audio: {str(e)}", status_code=400)

        content_type = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
        audio_content = response.content

        base_name = os.path.basename(url.split("?")[0])
        if "." in base_name:
            filename = base_name
        else:
            ext = CONTENT_TYPE_TO_EXT.get(content_type, "mp3")
            filename = f"{uuid.uuid4()}.{ext}"

        file_path = default_storage.save(f"audio_files/{filename}", ContentFile(audio_content))

        return {
            "file_path": file_path,
            "filename": os.path.basename(file_path),
            "file_size": len(audio_content),
            "content_type": content_type,
        }

