"""
api.py — Single endpoint: POST /tags/generate
         Input : event_description (required), event_name (optional)
         Output: tags list
"""

from fastapi import APIRouter, HTTPException
from app.schemas import TagRequest, TagResponse
from app.agent import generate_tags

router = APIRouter()


@router.post(
    "/tags/generate",
    response_model=TagResponse,
    summary="Generate Tags For Event",
    description=(
        "Send an event description (and optionally its name) and receive "
        "an AI-generated list of tags instantly. "
        "Called automatically by the backend for every new event created."
    ),
    tags=["Tags"],
)
def generate_event_tags(body: TagRequest):
    """
    ## Flow
    1. Backend creates/receives a new event from the database.
    2. Backend POSTs `event_description` (+ optional `event_name`) here.
    3. This service calls Groq (LLaMA 3.1 8B) and returns tags immediately.
    4. Backend saves the tags against the event record.

    ## Input
    | Field | Required | Max length |
    |---|---|---|
    | `event_description` | ✅ Yes | 5000 chars |
    | `event_name` | ❌ Optional | 300 chars |

    ## Output
    ```json
    { "tags": ["tag1", "tag2", "tag3"] }
    ```
    """
    try:
        tags = generate_tags(
            event_description=body.event_description,
            event_name=body.event_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=502, detail=f"Tag parsing error: {e}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"LLM request failed: {e}")

    return TagResponse(tags=tags)
