from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue, Range

from .embedder import Embedder


class Retriever:
    def __init__(self, client: QdrantClient, embedder: Embedder) -> None:
        self._client = client
        self._embedder = embedder

    def search_characters(
        self, query: str, location: str | None = None, top_k: int = 3
    ) -> list[dict]:
        filt = None
        if location:
            filt = Filter(must=[FieldCondition(key="location", match=MatchValue(value=location))])
        return self._search("characters", query, filt, top_k)

    def search_events(
        self, query: str, tick_max: int | None = None, top_k: int = 3
    ) -> list[dict]:
        filt = None
        if tick_max is not None:
            filt = Filter(must=[FieldCondition(key="tick", range=Range(lte=tick_max))])
        return self._search("events", query, filt, top_k)

    def search_world_rules(self, query: str, top_k: int = 3) -> list[dict]:
        return self._search("world_rules", query, None, top_k)

    def _search(
        self, collection: str, query: str, filt: Filter | None, top_k: int
    ) -> list[dict]:
        vec = self._embedder.embed(query)
        response = self._client.query_points(
            collection_name=collection,
            query=vec,
            query_filter=filt,
            limit=top_k,
        )
        return [r.payload["data"] for r in response.points]
