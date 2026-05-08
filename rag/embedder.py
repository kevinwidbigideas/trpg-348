from __future__ import annotations
import hashlib
import os
import numpy as np

EMBED_DIM = 1024  # bge-m3 output dimension


class Embedder:
    def __init__(self) -> None:
        self.mock = os.getenv("MOCK_LLM", "true").lower() == "true"
        if not self.mock:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(os.getenv("EMBED_MODEL", "BAAI/bge-m3"))

    def embed(self, text: str) -> list[float]:
        if self.mock:
            return _deterministic_vector(text)
        return self._model.encode(text, normalize_embeddings=True).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if self.mock:
            return [_deterministic_vector(t) for t in texts]
        return self._model.encode(texts, normalize_embeddings=True).tolist()


def _deterministic_vector(text: str) -> list[float]:
    seed = int(hashlib.md5(text.encode()).hexdigest(), 16) % (2**32)
    rng = np.random.default_rng(seed)
    vec = rng.standard_normal(EMBED_DIM).astype(np.float32)
    vec /= np.linalg.norm(vec)
    return vec.tolist()
