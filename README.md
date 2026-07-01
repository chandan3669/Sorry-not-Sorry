# ExcuseAI Backend

ExcuseAI is a FastAPI backend for generating AI-powered excuses with fake fun metrics and SQLite history.

## Features

- Generate excuses from category, audience, tone, and length
- Build dynamic Gemini prompts
- Return believability, drama, and risk scores
- Store generated excuses in SQLite
- Fetch and delete excuse history
- Environment-based API key loading with `python-dotenv`

## Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Do not commit `.env` or hardcode secrets.

## Run

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

## Endpoints

### `GET /`

Returns a welcome message.

### `GET /health`

Returns:

```json
{"status": "ok"}
```

### `POST /generate`

Request:

```json
{
  "category": "Missed class",
  "audience": "Professor",
  "tone": "Professional",
  "length": "Medium"
}
```

Response:

```json
{
  "excuse": "I apologize for missing class...",
  "believability": 87,
  "drama": 34,
  "risk": 18
}
```

If `GEMINI_API_KEY` is missing, the API returns a clean error:

```json
{
  "detail": "GEMINI_API_KEY not found"
}
```

### `GET /history`

Returns all saved excuses ordered by newest first.

### `DELETE /history/{id}`

Deletes a specific saved excuse.

## Project Structure

```text
backend/
|-- main.py
|-- routes/
|   `-- excuse.py
|-- services/
|   |-- ai_service.py
|   `-- score_service.py
|-- prompts/
|   `-- prompt_builder.py
|-- models/
|   `-- excuse_model.py
|-- schemas/
|   `-- excuse_schema.py
|-- database/
|   `-- db.py
|-- .env.example
|-- requirements.txt
`-- README.md
```
