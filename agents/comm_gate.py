from __future__ import annotations
from pydantic import BaseModel
from models import GameState


class CommResult(BaseModel):
    possible: bool
    delay_ticks: int = 0
    method: str = ""
    reason: str = ""


_BLOCKING_CONDITIONS = {"전투 중", "의식불명", "감금", "폐관"}

# 지역 간 전령 소요 tick
_TRAVEL_TICKS: dict[tuple[str, str], int] = {
    ("forest", "nameless_village"): 0,  # 인접
    ("nameless_village", "forest"): 0,
}


def _get_travel_ticks(loc_a: str, loc_b: str) -> int:
    return _TRAVEL_TICKS.get((loc_a, loc_b), _TRAVEL_TICKS.get((loc_b, loc_a), 3))


def can_communicate(
    char_a: str, char_b: str, game_state: GameState
) -> CommResult:
    state_a = game_state.get_character(char_a)
    state_b = game_state.get_character(char_b)

    if state_a is None or state_b is None:
        return CommResult(possible=False, reason="존재하지 않는 캐릭터입니다.")

    if not state_a.alive or not state_b.alive:
        return CommResult(possible=False, reason="사망한 캐릭터입니다.")

    # 물리적 상태 체크
    cond_b = state_b.condition
    for blocking in _BLOCKING_CONDITIONS:
        if blocking in cond_b:
            return CommResult(possible=False, reason=f"{state_b.name}이(가) {blocking} 상태입니다.")

    # 켄신: 심상공간에서만 소통 가능
    if char_b == "kenshin" or char_a == "kenshin":
        other = char_a if char_b == "kenshin" else char_b
        if other != "hajun":
            return CommResult(possible=False, reason="켄신은 하준의 심상공간에서만 소통 가능합니다.")
        return CommResult(possible=True, delay_ticks=0, method="심상공간", reason="")

    # hajun의 실제 위치는 game_state.active_location 사용
    loc_a = game_state.active_location if char_a == "hajun" else state_a.location
    loc_b = game_state.active_location if char_b == "hajun" else state_b.location

    # 같은 위치
    if loc_a == loc_b:
        return CommResult(possible=True, delay_ticks=0, method="직접 대화")

    # 다른 위치: 전령
    delay = _get_travel_ticks(loc_a, loc_b)
    return CommResult(possible=True, delay_ticks=delay, method="전령", reason=f"전령 {delay}tick 소요")
