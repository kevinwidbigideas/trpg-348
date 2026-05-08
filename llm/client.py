from __future__ import annotations
import os
from typing import AsyncIterator, Iterator


_MOCK_RESPONSE = "[MOCK] 헥터가 웃으며 고개를 끄덕였다."


class LLMClient:
    def __init__(self) -> None:
        self.mock = os.getenv("MOCK_LLM", "true").lower() == "true"
        if not self.mock:
            from openai import OpenAI
            self._client = OpenAI(
                base_url=os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1"),
                api_key="EMPTY",
            )
            self._model = os.getenv("VLLM_MODEL", "google/gemma-4-31B-it")

    def chat(self, messages: list[dict], **kwargs) -> str:
        if self.mock:
            return _MOCK_RESPONSE
        resp = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            **kwargs,
        )
        return resp.choices[0].message.content or ""

    def stream(self, messages: list[dict], **kwargs) -> Iterator[str]:
        if self.mock:
            for token in _MOCK_RESPONSE.split():
                yield token + " "
            return
        stream = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            stream=True,
            **kwargs,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta

    async def achat(self, messages: list[dict], **kwargs) -> str:
        if self.mock:
            return _MOCK_RESPONSE
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            base_url=os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1"),
            api_key="EMPTY",
        )
        resp = await client.chat.completions.create(
            model=self._model,
            messages=messages,
            **kwargs,
        )
        return resp.choices[0].message.content or ""

    async def astream(self, messages: list[dict], **kwargs) -> AsyncIterator[str]:
        if self.mock:
            for token in _MOCK_RESPONSE.split():
                yield token + " "
            return
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            base_url=os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1"),
            api_key="EMPTY",
        )
        stream = await client.chat.completions.create(
            model=self._model,
            messages=messages,
            stream=True,
            **kwargs,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta