from typing import Any
from dataclasses import dataclass
from src.models import get_reranking_model
from src.embeddings import profile_to_text

@dataclass
class RerankedProfile:
  score: float
  payload: dict[str, Any]

def rerank_profiles(query: str, profiles) -> list[RerankedProfile]:
  if not profiles:
    return []
  
  pairs = [[query, profile_to_text(profile)] for profile in profiles]
  scores = get_reranking_model().compute_score(pairs)
  
  ranked = sorted(
    zip(scores, profiles),
    key=lambda item: item[0],
    reverse=True
  )
  
  return [RerankedProfile(score=score, payload=profile) for score, profile in ranked]