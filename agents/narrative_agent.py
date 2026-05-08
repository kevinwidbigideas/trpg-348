from __future__ import annotations
import json
from pydantic import BaseModel
from agents.character_agent import CharacterResponse
from agents.dice_agent import RollResult
from llm.client import LLMClient
from models import GameState

_MOCK_STORY = """숲 속 공터. 어둠이 깔리기 시작한다.
갈색 머리의 소녀가 뛰쳐나오며 외쳤다.
"도망치세요!"

하준은 잠시 망설였지만, 몸이 먼저 움직였다."""

_MOCK_CHOICES = [
    "[A] 소녀를 뒤에 세우고 맞선다",
    "[B] 소녀를 데리고 도망친다",
    "[C] 소녀에게 먼저 도망치라고 한다",
]


class NarrativeOutput(BaseModel):
    story: str
    interface_logs: list[str]
    choices: list[str]


class NarrativeAgent:
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm

    def generate(
        self,
        event: str,
        game_state: GameState,
        char_responses: list[CharacterResponse] | None = None,
        roll_result: RollResult | None = None,
    ) -> NarrativeOutput:
        if self._llm.mock:
            return self._mock_generate(event, roll_result)
        return self._llm_generate(event, game_state, char_responses, roll_result)

    def _mock_generate(self, event: str, roll_result: RollResult | None) -> NarrativeOutput:
        logs: list[str] = []
        if roll_result:
            logs.append(roll_result.label)
        logs.append(f"<이벤트: {event}>")

        return NarrativeOutput(
            story=_MOCK_STORY,
            interface_logs=logs,
            choices=_MOCK_CHOICES,
        )

    def _llm_generate(
        self,
        event: str,
        game_state: GameState,
        char_responses: list[CharacterResponse] | None,
        roll_result: RollResult | None,
    ) -> NarrativeOutput:
        char_lines = ""
        if char_responses:
            char_lines = "\n".join(f"- {r.name}: {r.response}" for r in char_responses)

        roll_line = roll_result.label if roll_result else ""

        prompt = f"""당신은 소설 서술 에이전트입니다. 아래 정보를 바탕으로 한국어 소설 문체로 서술하세요.

이벤트: {event}
판정 결과: {roll_line}
인물 반응:
{char_lines}
현재 tick: {game_state.tick}
현재 위치: {game_state.active_location}

출력 형식 (JSON):
{{
  "story": "하준은...으로 시작하는 3~5문장 소설 서술",
  "interface_logs": ["<판정 결과>", "<퀘스트/칭호 알림>"],
  "choices": ["[A] ...", "[B] ...", "[C] ..."]
}}"""

        resp = self._llm.chat([{"role": "user", "content": prompt}])
        try:
            return NarrativeOutput(**json.loads(resp))
        except Exception:
            return self._mock_generate(event, roll_result)
