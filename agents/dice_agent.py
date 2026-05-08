from __future__ import annotations
import random
from pydantic import BaseModel


class RollResult(BaseModel):
    roll: int           # 1~100
    dc: int
    outcome: str        # 대성공 / 성공 / 실패 / 대실패
    label: str          # 인터페이스 출력용


def calculate_dc(
    base_dc: int,
    conditions: dict[str, bool | str] | None = None,
) -> int:
    modifier = 0
    if conditions:
        if conditions.get("target_sleeping"):
            modifier -= 25
        if conditions.get("darkness"):
            modifier -= 10
        if conditions.get("ally_nearby"):
            modifier -= 5
        if conditions.get("target_wounded"):
            modifier -= 10
        if conditions.get("power_gap") == "target_stronger":
            modifier += 10
        if conditions.get("power_gap") == "actor_stronger":
            modifier -= 15
    return max(5, min(95, base_dc + modifier))


def roll(dc: int, seed: int | None = None) -> RollResult:
    rng = random.Random(seed)
    value = rng.randint(1, 100)

    if value <= int(dc * 0.2):
        outcome, label = "대성공", f"<대성공> 완벽하게 해냈습니다. 추가 이점 발생."
    elif value <= dc:
        outcome, label = "성공", f"<성공> 의도한 대로 행동했습니다."
    elif value >= 95:
        outcome, label = "대실패", f"<대실패> 상황이 악화되었습니다."
    else:
        outcome, label = "실패", f"<실패> 뜻대로 되지 않았습니다."

    return RollResult(roll=value, dc=dc, outcome=outcome, label=label)
