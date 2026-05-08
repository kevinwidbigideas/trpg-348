from __future__ import annotations
import json
from pydantic import BaseModel
from llm.client import LLMClient
from models import GameState
from rag.retriever import Retriever


class ValidationResult(BaseModel):
    valid: bool
    partial: bool = False
    reason: str = ""
    alternatives: list[str] = []


# 금지 아이템 키워드 → (이유, 대안)
_FORBIDDEN: dict[str, tuple[str, list[str]]] = {
    "기관총": ("이 세계에는 화약/총기가 존재하지 않습니다.", ["석궁 발사", "마법 투사", "검술 공격"]),
    "총": ("이 세계에는 화약/총기가 존재하지 않습니다.", ["석궁 발사", "마법 투사", "검술 공격"]),
    "화약": ("이 세계에는 화약이 존재하지 않습니다.", ["마법 폭발", "불화살"]),
    "폭탄": ("이 세계에는 폭발물이 존재하지 않습니다.", ["마법 투사", "화염 마법"]),
    "전기": ("이 세계에는 전기 기술이 없습니다.", ["번개 마법", "조명 마법"]),
    "핸드폰": ("이 세계에는 현대 기술이 없습니다.", ["인터페이스 확인", "전령 파견"]),
    "스마트폰": ("이 세계에는 현대 기술이 없습니다.", ["인터페이스 확인"]),
    "자동차": ("이 세계에는 자동차가 없습니다.", ["말 탑승", "도보 이동"]),
}

# 이동 불가 지역 키워드 → (이유, 대안)
_OUT_OF_BOUNDS: dict[str, tuple[str, list[str]]] = {
    "로크빌": ("로크빌까지는 도보로 3일 거리입니다. 현재 장비/체력으로는 무리입니다.", ["마을에서 준비 후 출발", "헥터에게 동행 요청"]),
    "수도": ("신성제국 수도까지는 수 주 거리입니다.", ["현재 위치에서 정보 수집", "충분한 준비 후 출발"]),
    "신성제국": ("신성제국은 현재 1챕터 범위 밖입니다.", ["마을 내 활동", "숲 탐색"]),
}

# 서클 초과 마법 키워드
_HIGH_CIRCLE = ["2서클", "3서클", "4서클", "5서클", "고위 마법", "대마법"]


class Validator:
    def __init__(self, retriever: Retriever, llm: LLMClient) -> None:
        self._retriever = retriever
        self._llm = llm

    def validate(self, user_input: str, game_state: GameState) -> ValidationResult:
        if self._llm.mock:
            return self._mock_validate(user_input, game_state)
        return self._llm_validate(user_input, game_state)

    def _mock_validate(self, user_input: str, game_state: GameState) -> ValidationResult:
        for keyword, (reason, alts) in _FORBIDDEN.items():
            if keyword in user_input:
                return ValidationResult(valid=False, reason=reason, alternatives=alts)

        for place, (reason, alts) in _OUT_OF_BOUNDS.items():
            if place in user_input and ("이동" in user_input or "가" in user_input or "가겠" in user_input):
                return ValidationResult(valid=False, reason=reason, alternatives=alts)

        hajun = game_state.get_character("hajun")
        current_circle = int(hajun.extra.get("서클", 0)) if hajun else 0
        if any(kw in user_input for kw in _HIGH_CIRCLE) and current_circle == 0:
            return ValidationResult(
                valid=False,
                reason=f"현재 서클이 없어 해당 마법을 시전할 수 없습니다. (현재 서클: {current_circle})",
                alternatives=["수련을 통해 서클 습득", "켄신에게 지도 요청", "기본 신체 능력 활용"],
            )

        return ValidationResult(valid=True)

    def _llm_validate(self, user_input: str, game_state: GameState) -> ValidationResult:
        rules = self._retriever.search_world_rules(user_input, top_k=2)
        hajun = game_state.get_character("hajun")
        circle = int(hajun.extra.get("서클", 0)) if hajun else 0

        prompt = f"""당신은 348차원 세계관 검증 에이전트입니다.

세계관 규칙:
{json.dumps(rules, ensure_ascii=False, indent=2)}

플레이어 상태:
- 위치: {game_state.active_location}
- tick: {game_state.tick}
- 서클: {circle}

유저 행동: "{user_input}"

이 행동이 세계관 내에서 물리적으로 가능한지 판단하세요.
불가능하면 이유와 대안을, 부분 가능이면 약화된 버전을 제시하세요.

JSON으로만 응답: {{"valid": bool, "partial": bool, "reason": "string", "alternatives": ["string"]}}"""

        resp = self._llm.chat([{"role": "user", "content": prompt}])
        try:
            return ValidationResult(**json.loads(resp))
        except Exception:
            return ValidationResult(valid=True)
