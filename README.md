#SorryNotSorry AI Backend  

<p align="center">
  <img src="https://media.giphy.com/media/ZVik7pBtu9dNS/giphy.gif" width="180" />
</p>

<p align="center">
  <b>AI-powered excuse generation engine built with FastAPI + Gemini</b>
</p>

<p align="center">
  Generate smart excuses • Track history • Score believability
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.12-blue?logo=python"/>
<img src="https://img.shields.io/badge/FastAPI-Backend-green?logo=fastapi"/>
<img src="https://img.shields.io/badge/Gemini-AI-orange?logo=google"/>
<img src="https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite"/>
<img src="https://img.shields.io/badge/License-Educational-purple"/>
</p>

---

## Overview

ExcuseAI is a modern AI powered backend built with FastAPI that generates creative excuses based on user inputs such as category, audience, tone and length.

It integrates with Google Gemini API, generates fun scoring metrics and stores all excuses in SQLite for history tracking.

---

## Features

- AI-generated excuses using Gemini
- Dynamic prompt generation
- Believability, Drama & Risk scoring
- SQLite history storage
- Fetch and delete excuse history
- Secure environment variable support
- FastAPI Swagger docs
- Clean modular architecture
- Multiple AI response generation



## 🛠 Tech Stack

| Technology | Usage |
|---|---|
| Python | Core language |
| FastAPI | Backend framework |
| Gemini API | AI generation |
| SQLite | Database |
| SQLAlchemy | ORM |
| Pydantic | Validation |
| Uvicorn | Server |

---

## Project Structure

```bash
backend/
│── main.py
│── routes/
│   └── excuse.py
│── services/
│   ├── ai_service.py
│   └── score_service.py
│── prompts/
│   └── prompt_builder.py
│── models/
│   └── excuse_model.py
│── schemas/
│   └── excuse_schema.py
│── database/
│   └── db.py
│── .env.example
│── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd backend
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Setup

Create `.env`:

```bash
copy .env.example .env
```

Add your API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

⚠ Never commit `.env`

---

## ▶ Running the Server

```bash
uvicorn main:app --reload
```

Server URL:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Root

```http
GET /
```

Response:

```json
{
  "message": "ExcuseAI Backend Running"
}
```

---

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

### Generate Excuses

```http
POST /generate
```

Request:

```json
{
  "category": "Missed Class",
  "audience": "Professor",
  "tone": "Professional",
  "length": "Medium"
}
```

Response:

```json
{
  "responses": [
    {
      "id": 1,
      "text": "Excuse 1..."
    },
    {
      "id": 2,
      "text": "Excuse 2..."
    },
    {
      "id": 3,
      "text": "Excuse 3..."
    }
  ]
}
```

---

### Get History

```http
GET /history
```

Returns all saved excuses.

---

### Delete History

```http
DELETE /history/{id}
```

Deletes a saved excuse.

---

## Workflow

```text
    Frontend
   ↓
     API Request
   ↓
     FastAPI Backend
   ↓
     Prompt Builder
   ↓
     Gemini AI
   ↓
     Score Generator
   ↓
     SQLite Database
   ↓
     JSON Response
```

---

## Future Improvements

- AI Rewrite Mode
- Excuse Analyzer
- Authentication System
- Favorite Excuses
- Multi-language Support
- Custom Local LLM
- Fine-tuned Own Model
- AI Persona Mode

---

## Team — CONFUSION Stack

| Member | Role |
|---|---|
| Chandan | Backend Developer |
| Swapnil | AI Engineer |
| Ranab | Frontend Developer |
| Argha | UI/UX Designer |

---

##  License

Built for **educational** and **entertainment** purposes.

Use responsibly.

---

<p align="center">
Made with efforts by CONFUSION Stack
</p>
