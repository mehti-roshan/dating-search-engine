from src.config import BATCH_SIZE
from src.dataset import ESSAY_PROMPTS
from src.models import get_embedding_model

def _clean(value) -> str:
  """Convert a dataset value into clean text."""
  if value is None:
    return ""

  value = str(value).strip()

  # Treat common missing-value markers as empty.
  if value.lower() in {"", "nan", "none", "null"}:
    return ""

  return value

def profile_to_text(profile: dict) -> str:
  """
  Convert an OkCupid profile into descriptive text for embedding.

  Expects a dictionary containing the original dataset columns.
  """

  sections = []

  # Include useful descriptive attributes.
  attributes = {
    "Age": "age",
    "Gender": "sex",
    "Sexual orientation": "orientation",
    "Location": "location",
    "Education": "education",
    "Occupation": "job",
    "Body type": "body_type",
    "Diet": "diet",
    "Drinking habits": "drinks",
    "Smoking habits": "smokes",
    "Drug use": "drugs",
    "Languages spoken": "speaks",
    "Pets": "pets",
    "Children": "offspring",
    "Religion": "religion",
  }

  for label, field in attributes.items():
    value = _clean(profile.get(field))

    # The original dataset uses -1 for unknown income.
    if field == "income" and value == "-1":
      continue

    if value and value != "-1":
      sections.append(f"{label}: {value}")

  # Include the original essay responses with their prompts.
  for field, prompt in ESSAY_PROMPTS.items():
    essay = _clean(profile.get(field))

    if essay:
      sections.append(f"{prompt}: {essay}")

  return "\n".join(sections)

def embed_profiles(profile_texts):
  return get_embedding_model().encode(profile_texts, batch_size=BATCH_SIZE, normalize_embeddings=True, show_progress_bar=False)

def embed_query(query):
  instruction = (
    "Represent this sentence for searching relevant passages: "
  )
  return get_embedding_model().encode(
    [instruction + query],
    normalize_embeddings=True,
  )[0]