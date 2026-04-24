"""
agent.py — calls Groq Cloud (LLaMA 3.1 8B) with the event description
           and returns a list of tags.
"""

import re
import json
from groq import Groq
from app.config import settings

_client = Groq(api_key=settings.groq_api_key)


def generate_tags(event_description: str, event_name: str | None = None) -> list[str]:
    """
    Generate tags from an event description (and optionally its name).

    Args:
        event_description: the full text of the event (required).
        event_name:        title of the event (optional, improves quality).

    Returns:
        A list of lowercase tag strings.

    Raises:
        ValueError:  if the model response cannot be parsed.
        Exception:   on Groq API / network errors.
    """
    # Build the name line only when provided
    name_line = f"Event Name: {event_name}\n" if event_name else ""

    prompt = f"""You are an expert event categorization assistant.
Given the following event details, generate a list of relevant, concise tags
that best describe the event. Tags should be single words or short phrases (2-3 words max).
Return ONLY a valid JSON array of strings — no explanation, no markdown, no extra text.

{name_line}Event Description: {event_description}

Rules:
- Return between 3 and {settings.max_tags} tags.
- Tags must be lowercase.
- Tags must be relevant to the event content.
- Do NOT include generic words like "event" or "description".
- Output format exactly: ["tag1", "tag2", "tag3"]
"""

    response = _client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that generates tags for events. "
                    "You always respond with a valid JSON array of strings only. "
                    "Never add explanation or markdown."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        model=settings.groq_model,
        temperature=0.3,
        max_tokens=256,
    )

    raw = response.choices[0].message.content.strip()

    # Extract JSON array even if the model accidentally adds extra text
    match = re.search(r"\[.*?\]", raw, re.DOTALL)
    if not match:
        raise ValueError(f"Could not parse tags from model output: {raw!r}")

    tags = json.loads(match.group())

    if not isinstance(tags, list):
        raise ValueError("Model did not return a JSON list.")

    cleaned = [str(t).strip().lower() for t in tags if isinstance(t, str) and t.strip()]
    return cleaned[: settings.max_tags]
