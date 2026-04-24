# Event Tags AI Agent

AI micro-service for the ticketing platform.  
**Input →** event description &nbsp;|&nbsp; **Output →** tags list &nbsp;|&nbsp; **Live** for every new event.  

**Live API Documentation:** [Azure Deployment](https://event-tags-ai-tegy-e8aqexa5fcguacc2.uaenorth-01.azurewebsites.net/docs)

---

## How it works

```
Backend creates new event
        │
        ▼
POST /tags/generate
{ "event_description": "...", "event_name": "..." }
        │
        ▼
LLaMA 3.1 8B (Groq Cloud)
        │
        ▼
{ "tags": ["tag1", "tag2", ...] }
        │
        ▼
Backend saves tags to database
```

---

## Run

```powershell
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Swagger UI (Local) → **http://localhost:8000/docs**  
Swagger UI (Live) → [Azure Deployment](https://event-tags-ai-tegy-e8aqexa5fcguacc2.uaenorth-01.azurewebsites.net/docs)

---

## API

### `POST /tags/generate`

| Field | Required | Description |
|---|---|---|
| `event_description` | ✅ | Full event description |
| `event_name` | ❌ | Event title (improves quality) |

**Request:**
```json
{
  "event_description": "A 3-day outdoor music festival with live bands and food stalls.",
  "event_name": "Summer Fest"
}
```

**Response:**
```json
{
  "tags": ["music festival", "outdoor", "live bands", "food stalls", "summer"]
}
```

---

## Project Structure

```
Tags Model V2.0/
├── app/
│   ├── __init__.py
│   ├── config.py      ← loads .env settings
│   ├── schemas.py     ← request/response models
│   ├── agent.py       ← Groq LLM logic
│   └── api.py         ← POST /tags/generate endpoint
├── main.py            ← FastAPI entry point
├── .env               ← API key
└── requirements.txt
```
