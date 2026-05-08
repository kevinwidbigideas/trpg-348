from __future__ import annotations
import json
import pathlib
from models import GameState

SESSIONS_DIR = pathlib.Path("sessions")


def _branch_path(session_id: str) -> pathlib.Path:
    return SESSIONS_DIR / f"{session_id}_branches.json"


def _load_branches(session_id: str) -> list[dict]:
    p = _branch_path(session_id)
    if not p.exists():
        return []
    return json.loads(p.read_text(encoding="utf-8"))


def _save_branches(session_id: str, branches: list[dict]) -> None:
    SESSIONS_DIR.mkdir(exist_ok=True)
    _branch_path(session_id).write_text(
        json.dumps(branches, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def create_branch(
    game_state: GameState,
    divergence_summary: str,
    parent_branch: str | None = None,
) -> str:
    branches = _load_branches(game_state.session_id)
    branch_id = f"branch_{len(branches) + 1:03d}"

    branches.append({
        "branch_id": branch_id,
        "parent_branch": parent_branch,
        "tick": game_state.tick,
        "divergence_summary": divergence_summary,
        "character_states": {
            cid: {
                "alive": s.alive,
                "location": s.location,
                "condition": s.condition,
                "extra": s.extra,
            }
            for cid, s in game_state.character_states.items()
        },
    })
    _save_branches(game_state.session_id, branches)
    return branch_id


def restore_branch(session_id: str, branch_id: str) -> dict:
    branches = _load_branches(session_id)
    for b in branches:
        if b["branch_id"] == branch_id:
            return b
    raise KeyError(f"branch {branch_id!r} not found")


def get_tree(session_id: str) -> list[dict]:
    return _load_branches(session_id)
