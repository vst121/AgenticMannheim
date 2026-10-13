
from openai import OpenAI

from infrastructure.config.settings import settings


class OpenRouterClient:
    """Minimal client for OpenRouter's OpenAI-compatible API."""

    def __init__(self) -> None:
        self._model = settings.openrouter_model
        self._client = OpenAI(
            base_url=settings.openrouter_base_url,
            api_key=settings.openrouter_api_key,
        )

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )

        content = response.choices[0].message.content

        if not content or not content.strip():
            raise RuntimeError("The LLM returned an empty response.")

        return content.strip()
