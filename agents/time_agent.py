from __future__ import annotations
from enum import Enum
from models import GameState


class TimeMode(str, Enum):
    MACRO = "macro"
    MICRO = "micro"


# 이벤트가 발생하는 tick과 location — Micro 모드 판단 기준
_EVENT_LOCATIONS: dict[int, str] = {
    0: "void",
    1: "forest",
    2: "forest",
    3: "forest",
    4: "nameless_village",
    5: "nameless_village",
    6: "nameless_village",
}

# 반복 행동으로 판단할 키워드 (Macro 전환 트리거)
_IDLE_KEYWORDS = ["기다린다", "쉰다", "잠을 잔다", "반복", "그대로", "대기"]


def decide_mode(user_action: str, game_state: GameState) -> TimeMode:
    # 반복/대기 행동은 위치 무관하게 Macro
    if any(kw in user_action for kw in _IDLE_KEYWORDS):
        return TimeMode.MACRO

    # 유저 위치가 현재 tick 이벤트 위치와 일치하면 Micro
    event_loc = _EVENT_LOCATIONS.get(game_state.tick)
    if event_loc and game_state.active_location == event_loc:
        return TimeMode.MICRO

    return TimeMode.MACRO


def advance_time(game_state: GameState, mode: TimeMode) -> int:
    amount = 1 if mode == TimeMode.MICRO else 2
    return game_state.advance_tick(amount)


def ticks_until_next_event(game_state: GameState) -> int:
    next_ticks = [t for t in _EVENT_LOCATIONS if t > game_state.tick]
    if not next_ticks:
        return 0
    return min(next_ticks) - game_state.tick
