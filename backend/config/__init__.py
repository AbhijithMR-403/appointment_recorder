# Import Celery app so that "celery -A config worker/beat" finds it
from .celery import app

__all__ = ("app",)
