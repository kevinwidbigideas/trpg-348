"use client";

interface Props {
  tick: number;
  location: string;
  mode: string;
  branchId: string;
}

const LOCATION_KR: Record<string, string> = {
  forest: "이름없는 숲",
  nameless_village: "화전민 마을",
};

export default function StatusBar({ tick, location, mode, branchId }: Props) {
  return (
    <div className="pixel-box p-3 flex flex-wrap gap-x-6 gap-y-1 glow">
      <span>[ 348차원 ]</span>
      <span>TICK: <span className="glow-amber">{String(tick).padStart(2, "0")}</span></span>
      <span>LOC: <span style={{ color: "#44aaff" }}>{LOCATION_KR[location] ?? location}</span></span>
      <span>MODE: <span style={{ color: mode === "micro" ? "#00ff41" : "#ffb000" }}>
        {mode.toUpperCase()}
      </span></span>
      <span style={{ marginLeft: "auto", color: "#00aa2a", fontSize: "8px" }}>{branchId}</span>
    </div>
  );
}
