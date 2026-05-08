from __future__ import annotations
import asyncio
import json
import pathlib
from pydantic import BaseModel
from llm.client import LLMClient
from models import GameState
from rag.retriever import Retriever

# 정보 비대칭: 하준이 알 수 없는 비밀 (tick 조건)
_HIDDEN_SECRETS: dict[str, dict] = {
    "joy_josephine": {"secret": "신성제국 4황녀", "revealed_at_tick": 6},
}

# 캐릭터 페르소나 mock 응답
_MOCK_RESPONSES: dict[str, str] = {
    "hector": "호탕하게 웃으며 고개를 끄덕였다. \"꽤 하는군, 젊은이.\"",
    "joy_josephine": "조이가 밝게 웃으며 말했다. \"도와줘서 고마워요!\"",
    "matthew": "매튜가 뻐드렁니를 드러내며 웃었다. \"이 마을에 사연 없는 사람이 어디 있겠는가.\"",
    "kenshin": "- 그래도 어느정도 쓸 만해졌군. -",
    "shuned": "슈네드가 이를 갈며 외쳤다. \"헥터! 헥터!\"",
}


class CharacterResponse(BaseModel):
    character_id: str
    name: str
    response: str
    emotion: str = "neutral"


class CharacterAgent:
    def __init__(self, retriever: Retriever, llm: LLMClient) -> None:
        self._retriever = retriever
        self._llm = llm
        self._char_data: dict[str, dict] = {}
        self._load_char_data()

    def _load_char_data(self) -> None:
        chars_dir = pathlib.Path("data/ip/dimension_348/characters")
        for f in chars_dir.glob("*.json"):
            data = json.loads(f.read_text(encoding="utf-8"))
            self._char_data[data["character_id"]] = data

    def build_context(self, character_id: str, game_state: GameState) -> str:
        data = self._char_data.get(character_id, {})
        persona = data.get("persona", {})
        char_state = game_state.get_character(character_id)

        # RAG: 현재 위치/tick 기준 관련 이벤트 검색 (tick_max 적용 — 미래 오염 방지)
        events = self._retriever.search_events(
            f"{data.get('name', '')} 이벤트", tick_max=game_state.tick, top_k=2
        )

        # 정보 비대칭 적용: 비밀은 공개 tick 이전에 컨텍스트에서 제거
        secret_note = ""
        hidden = _HIDDEN_SECRETS.get(character_id)
        if hidden and game_state.tick < hidden["revealed_at_tick"]:
            secret_note = f"(주의: {hidden['secret']} 신분은 이 시점에 하준에게 미공개)"

        lines = [
            f"[{data.get('name', character_id)} 페르소나]",
            f"동기: {persona.get('motivation', '')}",
            f"말투: {persona.get('speech_style', '')}",
            f"현재 위치: {char_state.location if char_state else '불명'}",
            f"현재 상태: {char_state.condition if char_state else 'normal'}",
            secret_note,
            f"관련 이벤트: {[e.get('name') for e in events]}",
        ]
        return "\n".join(l for l in lines if l)

    async def react(
        self, character_id: str, event: str, game_state: GameState
    ) -> CharacterResponse:
        data = self._char_data.get(character_id, {})
        name = data.get("name", character_id)

        if self._llm.mock:
            response = _MOCK_RESPONSES.get(character_id, f"{name}이(가) 반응했다.")
            return CharacterResponse(character_id=character_id, name=name, response=response)

        context = self.build_context(character_id, game_state)
        resp = await self._llm.achat([
            {"role": "system", "content": context},
            {"role": "user", "content": f"이벤트: {event}\n이 캐릭터로서 한국어로 자연스럽게 반응하라."},
        ])
        return CharacterResponse(character_id=character_id, name=name, response=resp)


async def react_all(
    agent: CharacterAgent,
    location: str,
    event: str,
    game_state: GameState,
) -> list[CharacterResponse]:
    from game.state import get_active_characters
    active = get_active_characters(game_state)
    tasks = [agent.react(cid, event, game_state) for cid in active]
    return await asyncio.gather(*tasks)
