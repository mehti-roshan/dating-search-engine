import logging
from typing import Any
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from src.search import create_query_filter, search_profiles

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Dating Search")

class SearchRequest(BaseModel):
  query: str = Field(min_length=1, max_length=1000)
  limit: int = Field(default=10, ge=1, le=10)

  sex: str | None = None
  orientation: str | None = None
  status: str | None = None
  location: str | None = None

  min_age: int | None = Field(default=None, ge=18, le=100)
  max_age: int | None = Field(default=None, ge=18, le=100)

  min_height: int | None = Field(default=None, gt=0, le=98)
  max_height: int | None = Field(default=None, gt=0, le=98)

@app.post("/api/search")
def search(request: SearchRequest) -> dict[str, Any]:
  if (
    request.min_age is not None
    and request.max_age is not None
    and request.min_age > request.max_age
  ):
    raise HTTPException(
      status_code=422,
      detail="Minimum age cannot exceed maximum age.",
    )

  if (
    request.min_height is not None
    and request.max_height is not None
    and request.min_height > request.max_height
  ):
    raise HTTPException(
      status_code=422,
      detail="Minimum height cannot exceed maximum height.",
    )
  
  filters = request.model_dump(exclude_none=True, exclude={"query", "limit"})

  try:
    query_filter = create_query_filter(**filters)

    results = search_profiles(
      query=request.query,
      filter=query_filter,
      limit=request.limit,
    )

    return {
      "status": "success",
      "data": [
        {
          "score": point.score,
          "profile": point.payload,
        }
        for point in results
      ]
    }

  except Exception:
    logger.exception("Profile search failed")
    # Log the real exception on the server in a production app.
    raise HTTPException(
      status_code=500,
      detail="Search failed. Please try again.",
    ) from None

app.mount("/", StaticFiles(directory="static", html=True), name="static")