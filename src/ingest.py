from src.db import client, models
from src.dataset import profiles
from src.embeddings import profile_to_text, embed_profiles
from src.config import COLLECTION_NAME, BATCH_SIZE
from tqdm import tqdm
from uuid import uuid4

def ingest():
  batch = []

  for profile in tqdm(profiles, "Reading profiles"):
    batch.append(profile)

    if len(batch) >= BATCH_SIZE:
      upload_batch(batch)
      batch.clear()

  if batch:
    upload_batch(batch)

  print("Ingestion complete!")

def upload_batch(profiles):
  """Embed profiles and upload them to Qdrant."""
  texts = [profile_to_text(profile) for profile in profiles]
  vectors = embed_profiles(texts)

  points = []

  for profile, vector in zip(profiles, vectors):
    point_id = uuid4()

    points.append(
      models.PointStruct(
        id=point_id,
        vector=vector.tolist(),
        payload=profile,
      )
    )

  client.upload_points(collection_name=COLLECTION_NAME, points=points, batch_size=BATCH_SIZE, parallel=1, wait=True)

if __name__ == "__main__":
  ingest()