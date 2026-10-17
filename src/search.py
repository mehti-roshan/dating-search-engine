from src.db import client, models
from src.embeddings import embed_query
from src.reranking import rerank_profiles
from src.config import COLLECTION_NAME, USE_RERANKER

def create_query_filter(
  sex: str | None = None,
  status: str | None = None,
  orientation: str | None = None,
  body_type: str | None = None,
  diet: str | None = None,
  drinks: str | None = None,
  drugs: str | None = None,
  education: str | None = None,
  ethnicity: str | None = None,
  height: str | None = None,
  income: str | None = None,
  job: str | None = None,
  offspring: str | None = None,
  pets: str | None = None,
  religion: str | None = None,
  sign: str | None = None,
  smokes: str | None = None,
  location: str | None = None,
  min_age: int | None = None,
  max_age: int | None = None,
  min_height: int | None = None,
  max_height: int | None = None,
) -> models.Filter | None:
  conditions = []
  
  if sex is not None:
    conditions.append(models.FieldCondition(key="sex", match=models.MatchValue(value=sex)))

  if status is not None:
    conditions.append(models.FieldCondition(key="status", match=models.MatchValue(value=status)))

  if orientation is not None:
    conditions.append(models.FieldCondition(key="orientation", match=models.MatchValue(value=orientation)))

  if location is not None:
    conditions.append(models.FieldCondition(key="location", match=models.MatchValue(value=location)))
    
  if body_type is not None:
    conditions.append(models.FieldCondition(key="body_type", match=models.MatchValue(value=body_type)))
  
  if diet is not None:
    conditions.append(models.FieldCondition(key="diet", match=models.MatchValue(value=diet)))
  
  if drinks is not None:
    conditions.append(models.FieldCondition(key="drinks", match=models.MatchValue(value=drinks)))
  
  if drugs is not None:
    conditions.append(models.FieldCondition(key="drugs", match=models.MatchValue(value=drugs)))
  
  if education is not None:
    conditions.append(models.FieldCondition(key="education", match=models.MatchValue(value=education)))
  
  if ethnicity is not None:
    conditions.append(models.FieldCondition(key="ethnicity", match=models.MatchValue(value=ethnicity)))
  
  if height is not None:
    conditions.append(models.FieldCondition(key="height", match=models.MatchValue(value=height)))
  
  if income is not None:
    conditions.append(models.FieldCondition(key="income", match=models.MatchValue(value=income)))
  
  if job is not None:
    conditions.append(models.FieldCondition(key="job", match=models.MatchValue(value=job)))
  
  if offspring is not None:
    conditions.append(models.FieldCondition(key="offspring", match=models.MatchValue(value=offspring)))
  
  if pets is not None:
    conditions.append(models.FieldCondition(key="pets", match=models.MatchValue(value=pets)))
  
  if religion is not None:
    conditions.append(models.FieldCondition(key="religion", match=models.MatchValue(value=religion)))
  
  if sign is not None:
    conditions.append(models.FieldCondition(key="sign", match=models.MatchValue(value=sign)))
  
  if smokes is not None:
    conditions.append(models.FieldCondition(key="smokes", match=models.MatchValue(value=smokes)))
  
  if min_age is not None or max_age is not None:
    min_value = min_age if min_age is not None else 18
    max_value = max_age if max_age is not None else 100

    acceptable_ages = [
      str(age)
      for age in range(min_value, max_value + 1)
    ]

    conditions.append(
      models.FieldCondition(
        key="age",
        match=models.MatchAny(any=acceptable_ages),
      )
    )
  
  if min_height is not None or max_height is not None:
    min_value = min_height if min_height is not None else 1
    max_value = max_height if max_height is not None else 120

    acceptable_heights = [
      str(float(height))
      for height in range(min_value, max_value + 1)
    ]

    conditions.append(
      models.FieldCondition(
        key="height",
        match=models.MatchAny(any=acceptable_heights),
      )
    )
  
  return models.Filter(must=conditions) if conditions else None

def search_profiles(
  query: str,
  filter: models.Filter | None,
  limit: int = 10,
):
  query_embed = embed_query(query)
  points = client.query_points(collection_name=COLLECTION_NAME, query=query_embed, query_filter=filter, limit=limit, with_payload=True).points
  return points

def clamp(x, lower, upper):
  return max(lower, min(x, upper))

def search_profiles_reranker(
  query: str,
  filter: models.Filter | None,
  limit: int = 10,
  candidate_limit: int | None = None,
):
  if candidate_limit is None:
    candidate_limit = clamp(limit * 2, limit + 10, limit + 30)
  
  points = search_profiles(query=query, filter=filter, limit=candidate_limit)
  return rerank_profiles(query, [point.payload for point in points])[:limit]

def search_profiles_auto(
  query: str,
  filter: models.Filter | None,
  limit: int = 10,
  candidate_limit: int | None = None,
):
  if USE_RERANKER:
    return search_profiles_reranker(query=query, filter=filter, limit=limit)
  else:
    return search_profiles(query=query, filter=filter, limit=limit, candidate_limit=candidate_limit)

if __name__ == "__main__":
  query = input("Describe your ideal match: ")

  print(f"\n--- Query: {query} ---")
  filter = create_query_filter(sex='f')
  limit = 3

  results = search_profiles_auto(query=query, filter=filter, limit=limit)

  for i, point in enumerate(results, 1):
    print(f"\n--- Match {i} : Score: {point.score:.4f} ---")
    print(point.payload)