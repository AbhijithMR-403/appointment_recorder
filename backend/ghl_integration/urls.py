from django.urls import path
from .views import auth_connect, tokens, callback, webhook_handler


urlpatterns = [
    path("auth/connect/", auth_connect, name="oauth_connect"),
    path("auth/tokens/", tokens, name="oauth_tokens"),
    path("auth/callback/", callback, name="oauth_callback"),
    path("webhook/", webhook_handler, name="webhook"),
]