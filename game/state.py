from __future__ import annotations
import json
import pathlib
from models import CharacterState, GameState

# ip_schema 기반 근접 활성화 맵
# tick → 해당 tick에 유저 위치별로 활성화되는 캐릭터
_PROXIMITY_MAP: dict[int, dict[str, list[str]]] = {
    0: {"forest": []},
    1: {"forest": []},
    2: {"forest": ["joy_josephine"]},
    3: {"forest": ["hector", "joy_josephine"], "nameless_village": ["hector", "joy_josephine"]},
    4: {"nameless_village": ["hector", "joy_josephine", "matthew"]},
    5: {"nameless_village": ["hector", "joy_josephine", "kenshin", "shuned"]},
    6: {"nameless_village": ["hector", "joy_josephine"]},
}


def build_initial_state(session_id: str) -> GameState:
    ip_path = pathlib.Path("data/ip/dimension_348/characters")
    character_states: dict[str, CharacterState] = {}
    for f in ip_path.glob("*.json"):
        data = json.loads(f.read_text(encoding="utf-8"))
        init = data.get("initial_state", {})
        character_states[data["character_id"]] = CharacterState(
            character_id=data["character_id"],
            name=data["name"],
            location=init.get("location", "unknown"),
            alive=init.get("alive", True),
            accessible=init.get("accessible", True),
            condition=init.get("condition", "normal"),
            stats=data.get("stats", {}),
            relations=data.get("relations", {}),
            extra={k: v for k, v in init.items() if k not in ("location", "alive", "accessible", "condition")},
        )
    return GameState(
        session_id=session_id,
        tick=0,
        character_states=character_states,
        active_location="forest",
    )


def get_active_characters(game_state: GameState) -> list[str]:
    tick = min(game_state.tick, max(_PROXIMITY_MAP.keys()))
    location_map = _PROXIMITY_MAP.get(tick, {})
    return location_map.get(game_state.active_location, [])
