"use client";
import { useState, useCallback } from "react";
import StatusBar from "./StatusBar";
import NarrativeBox from "./NarrativeBox";
import ChoicePanel from "./ChoicePanel";
import { LogEntry } from "../../lib/types";
import { mockTurn } from "../../lib/api";

const INITIAL_CHOICES = [
  "[A] 주변을 탐색한다",
  "[B] 인터페이스를 확인한다",
  "[C] 냇가 방향으로 이동한다",
];

const INTRO_STORY = `눈을 떴을 때, 낯선 숲이었다.

머리가 지끈거렸다. 몸 어딘가에서 알림음이 울렸다.

[ 인터페이스 (EX) 권능이 활성화되었습니다. ]
[ 인도자를 탐색 중... ⚠ 오류 ]

하준은 천천히 일어나 주변을 둘러보았다.`;

export default function GameScreen() {
  const [tick, setTick] = useState(1);
  const [location] = useState("forest");
  const [mode, setMode] = useState("micro");
  const [branchId, setBranchId] = useState("branch_001");
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [choices, setChoices] = useState(INITIAL_CHOICES);
  const [isTyping, setIsTyping] = useState(true);
  const [currentStory, setCurrentStory] = useState(INTRO_STORY);
  const [currentLogs, setCurrentLogs] = useState<string[]>([
    "[ TICK 01 / 이름없는 숲 ]",
    "[ 인도자: ⚠ 오류 상태 ]",
  ]);
  const [processing, setProcessing] = useState(false);
  const [logId, setLogId] = useState(0);

  const handleSubmit = useCallback(async (input: string) => {
    if (processing) return;
    setProcessing(true);

    // 현재 서술을 로그로 이동
    setLogs((prev) => [
      ...prev,
      {
        id: logId,
        story: currentStory,
        interface_logs: currentLogs,
        user_input: input,
        tick,
      },
    ]);
    setLogId((n) => n + 1);
    setIsTyping(false);
    setCurrentStory("");
    setCurrentLogs([]);

    // 백엔드 호출 (현재는 mock)
    await new Promise((r) => setTimeout(r, 400)); // 처리 느낌
    const result = mockTurn(input, tick);

    setTick(result.tick_after);
    setMode(result.time_mode);
    if (result.branch_created) setBranchId(result.branch_created);
    setChoices(result.narrative.choices);
    setCurrentStory(result.narrative.story);
    setCurrentLogs(result.narrative.interface_logs);
    setIsTyping(true);
    setProcessing(false);
  }, [processing, currentStory, currentLogs, tick, logId]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        maxWidth: "860px",
        margin: "0 auto",
        padding: "16px",
        gap: "10px",
      }}
    >
      <StatusBar tick={tick} location={location} mode={mode} branchId={branchId} />

      <NarrativeBox
        logs={logs}
        isTyping={isTyping}
        currentStory={currentStory}
        currentLogs={currentLogs}
      />

      {processing && (
        <div style={{ textAlign: "center", color: "var(--green-dim)", fontSize: "9px" }}>
          <span style={{ animation: "blink 0.6s step-end infinite" }}>■</span>
          {" "}처리 중...
        </div>
      )}

      <ChoicePanel
        choices={choices}
        onSubmit={handleSubmit}
        disabled={processing || isTyping}
      />
    </div>
  );
}
