"""
schemas.py — Request / Response models for the tags endpoint.

The shape mirrors what the dbo.Events table provides:
  - event_name        → nvarchar / string  (optional — used to improve tag quality)
  - event_description → nvarchar / text    (required — the main input for tagging)
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class TagRequest(BaseModel):
    """
    What the backend sends to this service for every new event.

    Based on the Events table:
      - event_description  (required)  — the full text description of the event
      - event_name         (optional)  — helps the LLM generate more accurate tags
    """
    event_name: Optional[str] = Field(
        default=None,
        max_length=300,
        example="Summer Music Festival",
        description="Name / title of the event (optional but improves tag quality)",
    )
    event_description: str = Field(
        ...,
        min_length=5,
        max_length=5000,
        example="A 3-day outdoor music festival featuring local and international "
                "artists across multiple stages with food vendors and art exhibitions.",
        description="Full description of the event — REQUIRED",
    )


class TagResponse(BaseModel):
    """What this service returns to the backend."""
    tags: List[str] = Field(
        ...,
        example=["music festival", "outdoor", "live music", "food vendors"],
        description="List of AI-generated tags for the event",
    )
