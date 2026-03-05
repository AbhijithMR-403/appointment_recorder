import logging
from typing import Any

from anthropic import Anthropic
from decouple import config

from system_config.models import SystemSettings

logger = logging.getLogger(__name__)

DEFAULT_CLAUDE_MODEL = "claude-3-haiku-20240307"


def get_anthropic_client() -> Anthropic:
    """
    Return an Anthropic client using the API key from environment.
    """
    api_key = config("ANTHROPIC_API_KEY", default="")
    if not api_key:
        raise ValueError("Anthropic API key is not configured. Set ANTHROPIC_API_KEY.")
    return Anthropic(api_key=api_key)


class ClaudeAISummarizer:
    """
    Service class for generating summaries from appointment/call transcripts.

    Usage:
        summarizer = ClaudeAISummarizer(anthropic_client=my_client)
        summary = summarizer.summarize(transcription_text, initial_prompt=my_prompt)
    """

    def __init__(self, anthropic_client: Anthropic | None = None) -> None:
        self.settings = SystemSettings.get_settings()
        self.client = anthropic_client or get_anthropic_client()
        self.model_name = config("ANTHROPIC_MODEL", default=DEFAULT_CLAUDE_MODEL)
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
        Summarize a transcription using Claude (Anthropic).

        :param transcription_text: Full text of the transcription.
        :param initial_prompt: Instruction for how to summarize. If not provided,
            SystemSettings.summary_prompt or a built-in default will be used.
        :return: Summary text from the model (empty string on missing input).
        """
        if not transcription_text or not transcription_text.strip():
            return ""

        prompt = initial_prompt or self.default_prompt
        user_content = f"{transcription_text}"

        try:
            response: Any = self.client.messages.create(
                model=self.model_name,
                max_tokens=1024,
                system=prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_content,
                    },
                ],
                temperature=0.2,
            )
        except Exception:
            logger.exception("Failed to summarize transcription with Anthropic.")
            raise

        return (
            (response.content[0].text if response.content else "")
        ).strip()
