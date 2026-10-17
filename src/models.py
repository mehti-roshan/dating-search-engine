from src.config import EMBEDDING_MODEL, RERANKING_MODEL
from functools import lru_cache
from sentence_transformers import SentenceTransformer
from FlagEmbedding import FlagReranker

@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
  model = SentenceTransformer(EMBEDDING_MODEL, device="cpu")
  return model

@lru_cache(maxsize=1)
def get_reranking_model() -> FlagReranker:
  reranker = FlagReranker('BAAI/bge-reranker-large', use_fp16=True, normalize=True) # fp16 has minimal effect on error but increases performance
  return reranker