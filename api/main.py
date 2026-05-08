from __future__ import annotations
import pathlib
import sys
import os

# 프로젝트 루트를 path에 추가
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rag.embedder import Embedder
from rag.indexer import Indexer, get_qdrant_client
from rag.retriever import Retriever
from rag.dynamic_rag import DynamicRAG
from llm.client import LLMClient
from game.state import build_initial_state
from game import session as session_store
from agents.validator import Validator
from agents.character_agent import CharacterAgent
from agents.narrative_agent import NarrativeAgent
from agents.orchestrator import Orchestrator
from models import GameState

app = FastAPI(title="348차원 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 앱 시작 시 공유 리소스 초기화
_emb = Embedder()
_client = get_qdrant_client()
Indexer(_client, _emb).index_all(pathlib.Path("data/ip/dimension_348"))
_retriever = Retriever(_client, _emb)
_llm = LLMClient()
_dyn = DynamicRAG(_client, _emb)
_orc = Orchestrator(
    validator=Validator(_retriever, _llm),
    char_agent=CharacterAgent(_retriever, _llm),
    narrative_agent=NarrativeAgent(_llm),
    dynamic_rag=_dyn,
)

# 세션 인메모리 캐시 (session_id → GameState)
_sessions: dict[str, GameState] = {}


class StartRequest(BaseModel):
    session_id: str

class TurnRequest(BaseModel):
    user_input: str
    session_id: str


@app.get("/health")
def health():
    return {"status": "ok", "mock": _llm.mock}


@app.post("/start")
async def start(req: StartRequest):
    gs = build_initial_state(req.session_id)
    gs.tick = 1
    gs.active_location = "forest"
    _sessions[req.session_id] = gs
    return {
        "session_id": gs.session_id,
        "tick": gs.tick,
        "active_location": gs.active_location,
        "branch_id": gs.branch_id,
    }


@app.post("/turn")
async def turn(req: TurnRequest):
    gs = _sessions.get(req.session_id)
    if gs is None:
        raise HTTPException(status_code=404, detail="세션을 찾을 수 없습니다. /start 먼저 호출하세요.")
    result = await _orc.run_turn(req.user_input, gs)
    return result
