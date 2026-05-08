from __future__ import annotations
import hashlib
import time
from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue, Range, PointStruct, VectorParams, Distance
from .embedder import EMBED_DIM, Embedder
from models import DynamicChunk

COLLECTION = "dynamic_chunks"


def _chunk_id(chunk_id: str) -> int:
    return int(hashlib.md5(chunk_id.encode()).hexdigest()[:15], 16)


class DynamicRAG:
    def __init__(self, client: QdrantClient, embedder: Embedder) -> None:
        self._client = client
        self._embedder = embedder
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        existing = {c.name for c in self._client.get_collections().collections}
        if COLLECTION not in existing:
            self._client.create_collection(
                collection_name=COLLECTION,
                vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
            )

    def add_chunk(
        self,
        content: str,
        session_id: str,
        branch_id: str,
        tick: int,
        related_characters: list[str] | None = None,
        location: str = "",
        canon_divergence: bool = False,
    ) -> str:
        chunk_id = f"dyn_{session_id}_{branch_id}_{tick}_{int(time.time()*1000)}"
        vec = self._embedder.embed(content)
        self._client.upsert(
            collection_name=COLLECTION,
            points=[PointStruct(
                id=_chunk_id(chunk_id),
                vector=vec,
                payload={
                    "chunk_id": chunk_id,
                    "session_id": session_id,
                    "branch_id": branch_id,
                    "tick": tick,
                    "related_characters": related_characters or [],
                    "location": location,
                    "canon_divergence": canon_divergence,
                    "content": content,
                },
            )],
        )
        return chunk_id

    def search(
        self,
        query: str,
        session_id: str,
        branch_id: str,
        tick_max: int,
        top_k: int = 3,
    ) -> list[DynamicChunk]:
        vec = self._embedder.embed(query)
        filt = Filter(must=[
            FieldCondition(key="session_id", match=MatchValue(value=session_id)),
            FieldCondition(key="branch_id", match=MatchValue(value=branch_id)),
            FieldCondition(key="tick", range=Range(lte=tick_max)),
        ])
        response = self._client.query_points(
            collection_name=COLLECTION,
            query=vec,
            query_filter=filt,
            limit=top_k,
        )
        return [DynamicChunk(**r.payload) for r in response.points]
