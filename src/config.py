from os import getenv
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = getenv("COLLECTION_NAME", "dating_profiles")
EMBEDDING_MODEL = getenv("EMBEDDING_MODEL", "BAAI/bge-small-en-v1.5")
RERANKING_MODEL = getenv("RERANKING_MODEL", "BAAI/bge-reranker-base")
USE_RERANKER = getenv("USE_RERANKER", "false").lower() == 'true'
DATASET_NAME = getenv("DATASET_NAME", "SpiceeChat/OkCupid-59k-Anonymized-Profiles")
BATCH_SIZE = int(getenv("BATCH_SIZE", "64"))
VECTOR_SIZE = int(getenv("VECTOR_SIZE", "384"))