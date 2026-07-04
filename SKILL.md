# SorryNotSorry Backend Handoff

This document explains the full backend setup, API flow, authentication, database behavior, frontend integration, and known troubleshooting notes for the SorryNotSorry FastAPI backend.

## Project Path

```text
C:\Users\Chandan Barman\Desktop\sorry not sorry\backend
```

## Run Backend

Activate the virtual environment:

```powershell
cd "C:\Users\Chandan Barman\Desktop\sorry not sorry"
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
cd backend
```

Run for local and same-Wi-Fi access:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Local docs:

```text
http://127.0.0.1:8000/docs
```

Same-Wi-Fi docs:

```text
http://172.23.193.121:8000/docs
```

## Environment Variables

The backend uses `.env`.

Required:

```env
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Never commit or share `.env`.

## Base URL

Same laptop:

```text
http://127.0.0.1:8000
```

Frontend on another laptop on same Wi-Fi:

```text
http://172.23.193.121:8000
```

## Public Endpoints

### Health

```text
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Generate Excuses

```text
POST /generate
```

This endpoint is protected. It requires a JWT token so generated excuses can be saved under the correct user.

Headers:

```text
Authorization: Bearer JWT_TOKEN_HERE
```

Request body:

```json
{
  "category": "Missed class",
  "audience": "Professor",
  "tone": "Funny",
  "length": "Short"
}
```

Response body:

```json
{
  "responses": [
    {
      "id": 1,
      "text": "Excuse option one...",
      "believability": 91,
      "drama": 30,
      "risk": 15
    },
    {
      "id": 2,
      "text": "Excuse option two...",
      "believability": 84,
      "drama": 44,
      "risk": 20
    },
    {
      "id": 3,
      "text": "Excuse option three...",
      "believability": 77,
      "drama": 55,
      "risk": 28
    }
  ]
}
```

Important:

- Backend returns exactly 3 excuse options.
- Gemini is called once.
- Gemini is prompted to separate excuses using `###`.
- Backend parses the response and retries once if Gemini does not return exactly 3 excuses.
- Each generated option is saved as a normal history row owned by the logged-in user.

## Authentication Endpoints

### Register

```text
POST /auth/register
```

Request body:

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

Success response:

```json
{
  "message": "User registered successfully"
}
```

If user already exists:

```json
{
  "detail": "Email already registered"
}
```

### Login

```text
POST /auth/login
```

Request body:

```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

Success response:

```json
{
  "access_token": "JWT_TOKEN_HERE",
  "token_type": "bearer"
}
```

Invalid login response:

```json
{
  "detail": "Invalid email or password"
}
```

### Logout

```text
POST /auth/logout
```

This endpoint does not invalidate JWT server-side. Frontend should remove the stored token.

Success response:

```json
{
  "message": "Logged out successfully"
}
```

### Current User

```text
GET /auth/me
```

Headers:

```text
Authorization: Bearer JWT_TOKEN_HERE
```

Success response:

```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "created_at": "2026-07-02T10:30:00"
}
```

### Update Profile

```text
PUT /auth/profile
```

Headers:

```text
Authorization: Bearer JWT_TOKEN_HERE
```

Request body:

```json
{
  "username": "newusername",
  "email": "new@example.com"
}
```

Both fields are optional. Send only the field that should change.

Success response:

```json
{
  "message": "Profile updated successfully"
}
```

If email is already used by another account:

```json
{
  "detail": "Email already registered"
}
```

## JWT Token

The backend uses:

```text
HS256
```

Token expiry:

```text
60 minutes
```

Frontend should store the token:

```js
localStorage.setItem("token", loginData.access_token);
```

Protected routes need:

```text
Authorization: Bearer JWT_TOKEN_HERE
```

Example:

```js
const token = localStorage.getItem("token");

const res = await fetch("http://172.23.193.121:8000/history", {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
```

## Protected Endpoints

### Get History

```text
GET /history
```

Headers:

```text
Authorization: Bearer JWT_TOKEN_HERE
```

Success response:

```json
[
  {
    "id": 1,
    "excuse": "Saved excuse text...",
    "believability": 91,
    "drama": 30,
    "risk": 15,
    "category": "Missed class",
    "audience": "Professor",
    "tone": "Funny",
    "length": "Short",
    "created_at": "2026-07-02T10:30:00"
  }
]
```

Only excuses owned by the logged-in user are returned.

Unauthorized response:

```json
{
  "detail": "Not authenticated"
}
```

### Delete History Item

```text
DELETE /history/{excuse_id}
```

Example:

```text
DELETE /history/1
```

Headers:

```text
Authorization: Bearer JWT_TOKEN_HERE
```

Success response:

```json
{
  "message": "Excuse deleted successfully"
}
```

To find `excuse_id`, call `GET /history` and use the `id` field.

Users can delete only their own excuse records. Deleting another user's excuse returns `404`.

### Add Favorite

```text
POST /favorites
```

Headers:

```text
Authorization: Bearer JWT_TOKEN_HERE
```

Request body:

```json
{
  "excuse_id": 1
}
```

Success response:

```json
{
  "message": "Added to favorites"
}
```

Duplicate favorite response:

```json
{
  "detail": "Excuse already in favorites"
}
```

Users can favorite only their own excuse records.

### Get Favorites

```text
GET /favorites
```

Headers:

```text
Authorization: Bearer JWT_TOKEN_HERE
```

Success response:

```json
{
  "favorites": [
    {
      "id": 1,
      "excuse": "Saved excuse text...",
      "category": "Missed class",
      "tone": "Funny",
      "created_at": "2026-07-03T10:30:00"
    }
  ]
}
```

Only favorites owned by the logged-in user are returned.

### Delete Favorite

```text
DELETE /favorites/{id}
```

Headers:

```text
Authorization: Bearer JWT_TOKEN_HERE
```

Success response:

```json
{
  "message": "Favorite removed"
}
```

Users can remove only their own favorites.

## Frontend Fetch Examples

### Register

```js
await fetch("http://172.23.193.121:8000/auth/register", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    username: "testuser",
    email: "test@example.com",
    password: "password123",
  }),
});
```

### Login

```js
const loginRes = await fetch("http://172.23.193.121:8000/auth/login", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "test@example.com",
    password: "password123",
  }),
});

const loginData = await loginRes.json();
localStorage.setItem("token", loginData.access_token);
```

### Logout

```js
await fetch("http://172.23.193.121:8000/auth/logout", {
  method: "POST",
});

localStorage.removeItem("token");
```

### Current User

```js
const token = localStorage.getItem("token");

const res = await fetch("http://172.23.193.121:8000/auth/me", {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

const user = await res.json();
console.log(user);
```

### Update Profile

```js
const token = localStorage.getItem("token");

const res = await fetch("http://172.23.193.121:8000/auth/profile", {
  method: "PUT",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  },
  body: JSON.stringify({
    username: "newusername",
    email: "new@example.com",
  }),
});

const data = await res.json();
console.log(data);
```

### Generate

```js
const token = localStorage.getItem("token");

const res = await fetch("http://172.23.193.121:8000/generate", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  },
  body: JSON.stringify({
    category: "Missed class",
    audience: "Professor",
    tone: "Funny",
    length: "Short",
  }),
});

const data = await res.json();
console.log(data.responses);
```

### History

```js
const token = localStorage.getItem("token");

const res = await fetch("http://172.23.193.121:8000/history", {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

const history = await res.json();
console.log(history);
```

### Delete History

```js
const token = localStorage.getItem("token");
const excuseId = 1;

const res = await fetch(`http://172.23.193.121:8000/history/${excuseId}`, {
  method: "DELETE",
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

const data = await res.json();
console.log(data);
```

### Add Favorite

```js
const token = localStorage.getItem("token");

const res = await fetch("http://172.23.193.121:8000/favorites", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  },
  body: JSON.stringify({
    excuse_id: 1,
  }),
});

const data = await res.json();
console.log(data);
```

### Favorites

```js
const token = localStorage.getItem("token");

const res = await fetch("http://172.23.193.121:8000/favorites", {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

const data = await res.json();
console.log(data.favorites);
```

### Delete Favorite

```js
const token = localStorage.getItem("token");
const favoriteId = 1;

const res = await fetch(`http://172.23.193.121:8000/favorites/${favoriteId}`, {
  method: "DELETE",
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

const data = await res.json();
console.log(data);
```

## Database

SQLite database file:

```text
C:\Users\Chandan Barman\Desktop\sorry not sorry\backend\excuseai.db
```

Tables:

- `excuses`
- `users`
- `favorites`

SQLite does not run as a separate server. It is a file used by FastAPI.

## Current Models

### Excuse

Fields:

- id
- category
- audience
- tone
- length
- excuse
- believability
- drama
- risk
- created_at

### User

Fields:

- id
- username
- email
- hashed_password
- created_at

Passwords are hashed using bcrypt. Plain passwords are never stored.

### Favorite

Fields:

- id
- user_id
- excuse_id
- created_at

Favorites are unique by user and excuse.

## Current Gemini Setup

Gemini package:

```text
google-generativeai
```

Model:

```text
gemini-3.1-flash-lite
```

Timeout:

```text
15 seconds
```

Known warning:

```text
All support for the google.generativeai package has ended.
```

This warning does not stop the backend. It only means Google recommends migrating to `google.genai` later.

## Common Problems

### Frontend Cannot Connect

Check backend is running:

```text
http://172.23.193.121:8000/health
```

If it fails, run backend with:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

If still blocked, allow firewall:

```powershell
netsh advfirewall firewall add rule name="SorryNotSorry FastAPI 8000" dir=in action=allow protocol=TCP localport=8000
```

### History Returns 401

This is expected when no token is sent.

Fix:

```text
Authorization: Bearer JWT_TOKEN_HERE
```

### Register Returns 409

This means the email is already registered.

Use login, or register a different email.

### Generate Returns Gemini Quota Error

Gemini quota is controlled by Google AI Studio.

Check:

```text
https://ai.dev/rate-limit
```

Use a model with available quota. Current backend model:

```text
gemini-3.1-flash-lite
```

### Favicon 404

This is harmless:

```text
GET /favicon.ico 404 Not Found
```

Browsers request it automatically. It does not affect APIs.

## Implemented Backend Features

- FastAPI app
- CORS enabled
- SQLite database
- SQLAlchemy models
- Gemini AI integration
- Dynamic prompt builder
- Fake scores
- JWT auth
- bcrypt password hashing
- Protected user-owned history APIs
- Protected user-owned favorite APIs
- Auth profile APIs
- Protected generate API
- Swagger docs

## Not Implemented

JWT logout does not invalidate tokens on the backend. Frontend logout should delete the stored token after calling `/auth/logout`:

```js
localStorage.removeItem("token");
```
