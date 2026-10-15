from qdrant_client import QdrantClient, models
from src.config import QDRANT_URL, COLLECTION_NAME, VECTOR_SIZE

client = QdrantClient(QDRANT_URL)

def init_db() -> None:
  """Ensure the Qdrant collection and required indexes exist."""

  if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
      collection_name=COLLECTION_NAME,
      vectors_config=models.VectorParams(
        size=VECTOR_SIZE,
        distance=models.Distance.COSINE,
      ),
    )

    print(f"Created collection: {COLLECTION_NAME}")

  # Ensure payload indexes exist for frequently used filters.
  existing_indexes = (
    client.get_collection(COLLECTION_NAME)
    .payload_schema or {}
  )

  indexes = {
    "age": models.PayloadSchemaType.INTEGER,
    "city": models.PayloadSchemaType.KEYWORD,
    "interests": models.PayloadSchemaType.KEYWORD,
    "relationship_goal": models.PayloadSchemaType.KEYWORD,
  }

  for field, schema_type in indexes.items():
    if field not in existing_indexes:
      client.create_payload_index(
        collection_name=COLLECTION_NAME,
        field_name=field,
        field_schema=schema_type,
      )


# Initialize when this module is imported.
init_db()