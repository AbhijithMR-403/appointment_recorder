import logging
from typing import Any

from decouple import config
from openai import OpenAI

from system_config.models import SystemSettings

logger = logging.getLogger(__name__)


def get_openai_client() -> OpenAI:
    """
    Return an OpenAI client using the API key from SystemSettings,
    falling back to OPENAI_API_KEY in environment if needed.
    """
    settings = SystemSettings.get_settings()
    api_key = settings.openai_api_key or config("OPENAI_API_KEY", default="")
    if not api_key:
        raise ValueError("OpenAI API key is not configured.")
    return OpenAI(api_key=api_key)


class OpenAISummarizer:
    """
    Service class for generating summaries from appointment/call transcripts.

    Usage:
        summarizer = OpenAISummarizer(openai_client=my_client)
        summary = summarizer.summarize(transcription_text, initial_prompt=my_prompt)
    """

    def __init__(self, openai_client: OpenAI | None = None) -> None:
        self.settings = SystemSettings.get_settings()
        self.client = openai_client or get_openai_client()
        self.model_name = self.settings.openai_model or "gpt-4o-mini"
        self.default_prompt = (
            self.settings.summary_prompt
            or "Summarize the following transcript of an appointment or call. "
            "Include: main topics, decisions, action items, and any follow-up needed."
        )

    def summarize(
        self,
        transcription_text: str,
        initial_prompt: str | None = None,
    ) -> str:
        """
        Summarize a transcription using OpenAI.

        :param transcription_text: Full text of the transcription.
        :param initial_prompt: Instruction for how to summarize. If not provided,
            SystemSettings.summary_prompt or a built-in default will be used.
        :return: Summary text from the model (empty string on missing input).
        """
        if not transcription_text or not transcription_text.strip():
            return ""
        print(f"Transcription text: {transcription_text}\n")
        print(f"Initial prompt: {initial_prompt}\n")
        print(f"Default prompt: {self.default_prompt}\n")
        print(f"Prompt: {prompt}\n")
        print(f"User content: {user_content}\n")
        print(f"Model name: {self.model_name}\n")

        prompt = initial_prompt or self.default_prompt
        user_content = f"{transcription_text}"

        try:
            response: Any = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": prompt,
                    },
                    {
                        "role": "user",
                        "content": user_content,
                    },
                ],
                temperature=0.2,
            )
        except Exception:
            logger.exception("Failed to summarize transcription with OpenAI.")
            raise

        return (response.choices[0].message.content or "").strip()


