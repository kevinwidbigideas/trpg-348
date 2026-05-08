import sys
import io
import asyncio
import pathlib
import os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

from dotenv import load_dotenv
load_dotenv()

from rag.embedder import Embedder
from rag.indexer import Indexer, get_qdrant_client
from rag.retriever import Retriever
from rag.dynamic_rag import DynamicRAG
from llm.client import LLMClient
from game.state import build_initial_state
from game import session, branch
from agents.validator import Validator
from agents.character_agent import CharacterAgent
from agents.narrative_agent import NarrativeAgent
from agents.orchestrator import Orchestrator

DIVIDER = "━" * 40


def _setup() -> Orchestrator:
    emb = Embedder()
    client = get_qdrant_client()
    Indexer(client, emb).index_all(pathlib.Path("data/ip/dimension_348"))
    retriever = Retriever(client, emb)
    llm = LLMClient()
    dyn = DynamicRAG(client, emb)
    return Orchestrator(
        validator=Validator(retriever, llm),
        char_agent=CharacterAgent(retriever, llm),
        narrative_agent=NarrativeAgent(llm),
        dynamic_rag=dyn,
    )


def _print_tree(session_id: str) -> None:
    tree = branch.get_tree(session_id)
    if not tree:
        return
    print("\n[분기 트리]")
    for b in tree:
        parent = b["parent_branch"] or "root"
        print(f"  {parent} → {b['branch_id']} [tick {b['tick']}] {b['divergence_summary']}")


def _print_narrative(narrative) -> None:
    print(f"\n{DIVIDER}")
    print("📖 [서술]")
    print(narrative.story)
    for log in narrative.interface_logs:
        print(log)
    print(DIVIDER)
    print("다음 행동:")
    for choice in narrative.choices:
        print(f"  {choice}")
    print("  [직접 입력]")


async def _game_loop(orc: Orchestrator, game_state) -> None:
    print(f"\n=== 348차원 — tick {game_state.tick} / {game_state.active_location} ===")
    while True:
        user_input = input("\n> ").strip()
        if not user_input:
            continue
        if user_input in ("q", "quit", "종료"):
            print("게임을 종료합니다.")
            break
        if user_input == "tree":
            _print_tree(game_state.session_id)
            continue

        result = await orc.run_turn(user_input, game_state)
        _print_narrative(result.narrative)
        print(f"[tick {result.tick_after} / {game_state.active_location}]")
        if result.branch_created:
            print(f"<분기 저장: {result.branch_created}>")


def main() -> None:
    mock = os.getenv("MOCK_LLM", "true").lower() == "true"
    print("348차원 소설 세계관 체험 시스템")
    print(f"모드: {'MOCK' if mock else 'REAL'} | 모델: {os.getenv('VLLM_MODEL', '-')}")
    print(DIVIDER)
    print("[1] 새 게임  [2] 불러오기")
    choice = input("> ").strip()

    orc = _setup()

    if choice == "2":
        session_id = input("세션 ID: ").strip()
        try:
            gs = session.load(session_id)
            print(f"세션 로드: tick {gs.tick}")
        except FileNotFoundError:
            print("세션을 찾을 수 없습니다. 새 게임을 시작합니다.")
            gs = build_initial_state("new_game")
    else:
        gs = build_initial_state("new_game")
        gs.tick = 2
        gs.active_location = "forest"

    asyncio.run(_game_loop(orc, gs))


if __name__ == "__main__":
    main()
