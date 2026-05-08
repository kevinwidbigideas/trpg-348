from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field


class CharacterState(BaseModel):
    character_id: str
    name: str
    location: str
    alive: bool = True
    accessible: bool = True
    condition: str = "normal"
    stats: dict[str, Any] = Field(default_factory=dict)
    relations: dict[str, Any] = Field(default_factory=dict)
    extra: dict[str, Any] = Field(default_factory=dict)


class CanonEvent(BaseModel):
    event_id: str
    tick: int
    location: str
    name: str
    description: str
    importance: str  # critical / high / medium / low
    divergence_possible: bool
    involved_characters: list[str]
    canon_outcome: str
    divergence_options: list[str] = Field(default_factory=list)
    causality: dict[str, Any] = Field(default_factory=dict)


class WorldRule(BaseModel):
    rule_id: str
    category: str  # magic / combat / technology / communication
    content: dict[str, Any]


class Location(BaseModel):
    id: str
    name: str
    type: str
    accessible: bool
    description: str
    adjacent: list[str] = Field(default_factory=list)
    danger_level: str = "low"
    note: str = ""


class GameState(BaseModel):
    session_id: str
    branch_id: str = "branch_001"
    tick: int = 0
    character_states: dict[str, CharacterState] = Field(default_factory=dict)
    ip_id: str = "dimension_348_v1"
    active_location: str = "forest"

    def get_character(self, character_id: str) -> Optional[CharacterState]:
        return self.character_states.get(character_id)

    def update_character(self, character_id: str, **kwargs: Any) -> None:
        state = self.character_states.get(character_id)
        if state is None:
            raise KeyError(f"character {character_id!r} not in game state")
        updated = state.model_copy(update=kwargs)
        self.character_states[character_id] = updated

    def advance_tick(self, amount: int = 1) -> int:
        self.tick += amount
        return self.tick

    def get_nearby_characters(self, location: str) -> list[str]:
        return [
            cid for cid, state in self.character_states.items()
            if state.location == location and state.accessible and cid != "hajun"
        ]


class DynamicChunk(BaseModel):
    chunk_id: str
    session_id: str
    branch_id: str
    tick: int
    related_characters: list[str] = Field(default_factory=list)
    location: str
    canon_divergence: bool = False
    content: str
    embedding: Optional[list[float]] = None
