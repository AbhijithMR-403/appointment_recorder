from django.urls import path

from .views import RevCallbackView

urlpatterns = [
    path("rev/callback/", RevCallbackView.as_view(), name="rev_callback"),
]
