from __future__ import annotations
import json
import pathlib
from models import GameState

SESSIONS_DIR = pathlib.Path("sessions")


def save(game_state: GameState) -> pathlib.Path:
    SESSIONS_DIR.mkdir(exist_ok=True)
    path = SESSIONS_DIR / f"{game_state.session_id}.json"
    path.write_text(game_state.model_dump_json(indent=2), encoding="utf-8")
    return path


def load(session_id: str) -> GameState:
    path = SESSIONS_DIR / f"{session_id}.json"
    return GameState.model_validate_json(path.read_text(encoding="utf-8"))
