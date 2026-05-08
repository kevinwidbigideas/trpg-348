import { TurnResult, GameState } from "./types";

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function startGame(session_id: string): Promise<GameState> {
  const res = await fetch(`${BASE}/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id }),
  });
  if (!res.ok) throw new Error("start failed");
  return res.json();
}

export async function sendTurn(
  user_input: string,
  session_id: string
): Promise<TurnResult> {
  const res = await fetch(`${BASE}/turn`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ user_input, session_id }),
  });
  if (!res.ok) throw new Error("turn failed");
  return res.json();
}

// 백엔드 없을 때 사용하는 mock
export function mockTurn(user_input: string, tick: number): TurnResult {
  const outcomes = ["성공", "실패", "대성공", "대실패"];
  const outcome = outcomes[Math.floor(Math.random() * outcomes.length)];
  const labelMap: Record<string, string> = {
    "대성공": "<대성공> 완벽하게 해냈습니다. 추가 이점 발생.",
    "성공":   "<성공> 의도한 대로 행동했습니다.",
    "실패":   "<실패> 뜻대로 되지 않았습니다.",
    "대실패": "<대실패> 상황이 악화되었습니다.",
  };
  return {
    validation: { valid: true, reason: "", alternatives: [] },
    time_mode: "micro",
    roll_result: { roll: Math.floor(Math.random() * 100) + 1, dc: 50, outcome, label: labelMap[outcome] },
    narrative: {
      story: `하준은 "${user_input}"을(를) 시도했다.\n숲 속 공터. 어둠이 깔리기 시작한다.\n갈색 머리의 소녀가 뛰쳐나오며 외쳤다. "도망치세요!"`,
      interface_logs: [labelMap[outcome], `<이벤트: ${user_input}>`],
      choices: ["[A] 소녀를 뒤에 세우고 맞선다", "[B] 소녀를 데리고 도망친다", "[C] 소녀에게 먼저 도망치라고 한다"],
    },
    tick_after: tick + 1,
    branch_created: outcome === "대성공" || outcome === "대실패" ? `branch_00${tick}` : null,
  };
}
