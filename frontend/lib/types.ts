export interface TurnResult {
  validation: { valid: boolean; reason: string; alternatives: string[] };
  time_mode: "micro" | "macro";
  roll_result: { roll: number; dc: number; outcome: string; label: string } | null;
  narrative: {
    story: string;
    interface_logs: string[];
    choices: string[];
  };
  tick_after: number;
  branch_created: string | null;
}

export interface GameState {
  session_id: string;
  tick: number;
  active_location: string;
  branch_id: string;
}

export interface LogEntry {
  id: number;
  story: string;
  interface_logs: string[];
  user_input: string;
  tick: number;
}
