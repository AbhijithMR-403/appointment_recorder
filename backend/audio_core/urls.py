from django.urls import path

from .views import AudioFileListView, UploadAudioView

urlpatterns = [
    path("upload/", UploadAudioView.as_view(), name="upload_audio"),
    path("", AudioFileListView.as_view(), name="list_audio_files"),
]
