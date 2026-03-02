from django.urls import path

from .views import RevCallbackView, TranscriptionLogListView

urlpatterns = [
    path("rev/callback/", RevCallbackView.as_view(), name="rev_callback"),
    path("transcription-logs/", TranscriptionLogListView.as_view(), name="transcription_log_list"),
]
