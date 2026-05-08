from __future__ import annotations
import hashlib
import json
import os
import pathlib

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from .embedder import EMBED_DIM, Embedder

COLLECTIONS = ["characters", "events", "world_rules", "locations"]


def get_qdrant_client() -> QdrantClient:
    if os.getenv("MOCK_LLM", "true").lower() == "true":
        return QdrantClient(":memory:")
    return QdrantClient(
        host=os.getenv("QDRANT_HOST", "localhost"),
        port=int(os.getenv("QDRANT_PORT", 6333)),
    )


def _str_id(s: str) -> int:
    return int(hashlib.md5(s.encode()).hexdigest()[:15], 16)


class Indexer:
    def __init__(self, client: QdrantClient, embedder: Embedder) -> None:
        self._client = client
        self._embedder = embedder

    def setup_collections(self) -> None:
        existing = {c.name for c in self._client.get_collections().collections}
        for name in COLLECTIONS:
            if name not in existing:
                self._client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(size=EMBED_DIM, distance=Distance.COSINE),
                )

    def index_all(self, ip_path: pathlib.Path) -> None:
        self.setup_collections()
        self._index_characters(ip_path / "characters")
        self._index_events(ip_path / "timeline" / "canon_events.json")
        self._index_world_rules(ip_path / "world")
        self._index_locations(ip_path / "world" / "geography.json")

    def _index_characters(self, chars_dir: pathlib.Path) -> None:
        points = []
        for f in chars_dir.glob("*.json"):
            data = json.loads(f.read_text(encoding="utf-8"))
            persona = data.get("persona", {})
            text = f"{data['name']} {persona.get('motivation', '')} {persona.get('speech_style', '')}"
            init = data.get("initial_state", {})
            points.append(PointStruct(
                id=_str_id(data["character_id"]),
                vector=self._embedder.embed(text),
                payload={
                    "character_id": data["character_id"],
                    "name": data["name"],
                    "tier": data.get("tier"),
                    "location": init.get("location"),
                    "data": data,
                },
            ))
        self._client.upsert(collection_name="characters", points=points)

    def _index_events(self, events_file: pathlib.Path) -> None:
        data = json.loads(events_file.read_text(encoding="utf-8"))
        points = []
        for evt in data["events"]:
            text = f"{evt['name']} {evt['description']}"
            points.append(PointStruct(
                id=_str_id(evt["event_id"]),
                vector=self._embedder.embed(text),
                payload={
                    "event_id": evt["event_id"],
                    "tick": evt["tick"],
                    "location": evt["location"],
                    "importance": evt["importance"],
                    "involved_characters": evt["involved_characters"],
                    "data": evt,
                },
            ))
        self._client.upsert(collection_name="events", points=points)

    def _index_world_rules(self, world_dir: pathlib.Path) -> None:
        points = []
        for i, f in enumerate(world_dir.glob("*.json")):
            if f.name == "geography.json":
                continue
            data = json.loads(f.read_text(encoding="utf-8"))
            text = json.dumps(data, ensure_ascii=False)[:600]
            points.append(PointStruct(
                id=_str_id(f.stem),
                vector=self._embedder.embed(text),
                payload={"category": f.stem, "data": data},
            ))
        self._client.upsert(collection_name="world_rules", points=points)

    def _index_locations(self, geo_file: pathlib.Path) -> None:
        data = json.loads(geo_file.read_text(encoding="utf-8"))
        points = []
        for loc in data["locations"]:
            text = f"{loc['name']} {loc['description']}"
            points.append(PointStruct(
                id=_str_id(loc["id"]),
                vector=self._embedder.embed(text),
                payload={
                    "location_id": loc["id"],
                    "name": loc["name"],
                    "adjacent": loc["adjacent"],
                    "data": loc,
                },
            ))
        self._client.upsert(collection_name="locations", points=points)
