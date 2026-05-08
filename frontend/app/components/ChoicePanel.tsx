"use client";
import { useRef, useState } from "react";

interface Props {
  choices: string[];
  onSubmit: (input: string) => void;
  disabled: boolean;
}

export default function ChoicePanel({ choices, onSubmit, disabled }: Props) {
  const [customInput, setCustomInput] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  function handleChoice(c: string) {
    if (disabled) return;
    onSubmit(c.replace(/^\[.\]\s*/, ""));
  }

  function handleCustom(e: React.FormEvent) {
    e.preventDefault();
    if (!customInput.trim() || disabled) return;
    onSubmit(customInput.trim());
    setCustomInput("");
  }

  return (
    <div className="pixel-box p-4" style={{ borderTop: "2px solid var(--green-dim)" }}>
      <div style={{ marginBottom: "10px", color: "#00aa2a", fontSize: "8px" }}>
        ▼ 다음 행동
      </div>

      {choices.map((c, i) => (
        <button key={i} className="choice-btn" onClick={() => handleChoice(c)} disabled={disabled}>
          {c}
        </button>
      ))}

      <form onSubmit={handleCustom} style={{ marginTop: "10px", display: "flex", alignItems: "center", gap: "8px" }}>
        <span className="glow" style={{ whiteSpace: "nowrap" }}>{">"}</span>
        <input
          ref={inputRef}
          className="game-input"
          value={customInput}
          onChange={(e) => setCustomInput(e.target.value)}
          placeholder="직접 입력..."
          disabled={disabled}
          autoComplete="off"
        />
        <button
          type="submit"
          disabled={disabled}
          style={{
            background: "transparent",
            border: "2px solid var(--green-dim)",
            color: "var(--green)",
            fontFamily: "'Press Start 2P', monospace",
            fontSize: "9px",
            padding: "6px 10px",
            cursor: disabled ? "not-allowed" : "pointer",
            whiteSpace: "nowrap",
          }}
        >
          실행
        </button>
      </form>
    </div>
  );
}
