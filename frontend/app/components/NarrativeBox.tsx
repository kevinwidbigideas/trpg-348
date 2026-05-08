"use client";
import { useEffect, useRef, useState } from "react";
import { LogEntry } from "../../lib/types";

interface Props {
  logs: LogEntry[];
  isTyping: boolean;
  currentStory: string;
  currentLogs: string[];
}

function getLogClass(log: string): string {
  if (log.includes("대성공")) return "iface-critical";
  if (log.includes("성공"))   return "iface-success";
  if (log.includes("실패"))   return "iface-failure";
  if (log.includes("퀘스트") || log.includes("칭호") || log.includes("이벤트")) return "iface-info";
  return "iface-info";
}

function TypewriterText({ text, onDone }: { text: string; onDone?: () => void }) {
  const [displayed, setDisplayed] = useState("");
  useEffect(() => {
    setDisplayed("");
    let i = 0;
    const id = setInterval(() => {
      if (i >= text.length) { clearInterval(id); onDone?.(); return; }
      setDisplayed(text.slice(0, i + 1));
      i++;
    }, 18);
    return () => clearInterval(id);
  }, [text]);
  return <span style={{ whiteSpace: "pre-wrap" }}>{displayed}<span style={{ animation: "blink 1s step-end infinite" }}>█</span></span>;
}

export default function NarrativeBox({ logs, isTyping, currentStory, currentLogs }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs, currentStory]);

  return (
    <div className="pixel-box p-4 flex-1 overflow-y-auto" style={{ minHeight: 0 }}>
      {/* 지난 로그 */}
      {logs.map((entry) => (
        <div key={entry.id} style={{ marginBottom: "16px", opacity: 0.6 }}>
          <div style={{ color: "#00aa2a", marginBottom: "4px", fontSize: "8px" }}>
            ▶ {entry.user_input} [tick {entry.tick}]
          </div>
          <div style={{ whiteSpace: "pre-wrap", marginBottom: "8px", color: "#00cc33" }}>
            {entry.story}
          </div>
          {entry.interface_logs.map((log, i) => (
            <div key={i} className={getLogClass(log)} style={{ marginBottom: "2px" }}>
              {log}
            </div>
          ))}
          <hr className="pixel-divider" />
        </div>
      ))}

      {/* 현재 진행 중인 서술 */}
      {isTyping && (
        <div>
          <div style={{ whiteSpace: "pre-wrap", marginBottom: "8px" }} className="glow">
            <TypewriterText text={currentStory} />
          </div>
          {currentLogs.map((log, i) => (
            <div key={i} className={getLogClass(log)} style={{ marginBottom: "2px" }}>
              {log}
            </div>
          ))}
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
