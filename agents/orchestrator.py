from __future__ import annotations
from pydantic import BaseModel
from agents.character_agent import CharacterAgent, react_all
from agents.comm_gate import can_communicate
from agents.dice_agent import RollResult, calculate_dc, roll
from agents.narrative_agent import NarrativeAgent, NarrativeOutput
from agents.time_agent import TimeMode, advance_time, decide_mode
from agents.validator import ValidationResult, Validator
from game import branch, session
from models import GameState
from rag.dynamic_rag import DynamicRAG


class TurnResult(BaseModel):
    validation: ValidationResult
    time_mode: TimeMode
    roll_result: RollResult | None
    narrative: NarrativeOutput
    tick_after: int
    branch_created: str | None = None


class Orchestrator:
    def __init__(
        self,
        validator: Validator,
        char_agent: CharacterAgent,
        narrative_agent: NarrativeAgent,
        dynamic_rag: DynamicRAG,
    ) -> None:
        self._validator = validator
        self._char_agent = char_agent
        self._narrative = narrative_agent
        self._dyn_rag = dynamic_rag

    async def run_turn(self, user_input: str, game_state: GameState) -> TurnResult:
        # 1. 세계관 검증
        validation = self._validator.validate(user_input, game_state)
        if not validation.valid and not validation.partial:
            narrative = self._narrative.generate(user_input, game_state)
            narrative.story = f"<행동 불가>\n{validation.reason}\n가능한 행동: {validation.alternatives}"
            narrative.choices = [f"[{c}]" for c in validation.alternatives[:3]]
            return TurnResult(
                validation=validation,
                time_mode=TimeMode.MICRO,
                roll_result=None,
                narrative=narrative,
                tick_after=game_state.tick,
            )

        # 2. 시간 모드 결정
        time_mode = decide_mode(user_input, game_state)

        # 3. 주사위 판정 (기본 DC 50)
        roll_result = roll(calculate_dc(50))

        # 4. 인물 에이전트 병렬 실행
        char_responses = await react_all(
            self._char_agent, game_state.active_location, user_input, game_state
        )

        # 5. 상태 업데이트 + 동적 RAG
        advance_time(game_state, time_mode)
        self._dyn_rag.add_chunk(
            content=f"[tick {game_state.tick}] {user_input} → {roll_result.outcome}",
            session_id=game_state.session_id,
            branch_id=game_state.branch_id,
            tick=game_state.tick,
            location=game_state.active_location,
        )

        # 6. critical 이벤트면 분기 자동 저장
        branch_id = None
        if roll_result.outcome in ("대성공", "대실패"):
            branch_id = branch.create_branch(
                game_state,
                divergence_summary=f"{user_input} ({roll_result.outcome})",
                parent_branch=game_state.branch_id,
            )
            game_state.branch_id = branch_id
            session.save(game_state)

        # 7. 내러티브 생성
        narrative = self._narrative.generate(
            user_input, game_state, char_responses, roll_result
        )

        return TurnResult(
            validation=validation,
            time_mode=time_mode,
            roll_result=roll_result,
            narrative=narrative,
            tick_after=game_state.tick,
            branch_created=branch_id,
        )
